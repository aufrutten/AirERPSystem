from datetime import date
from typing import TYPE_CHECKING

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager

from celery import current_app as celery_current_app
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .. import fields
from ..utils import get_context, check_token, current_time_timedelta

if TYPE_CHECKING:
    from ..tasks import send_email_celery


class UserManager(BaseUserManager):

    def _create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        kwargs.setdefault('photo', None)
        kwargs.setdefault('is_active', False)
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        return user

    def create_user(self, email, password=None, **kwargs):
        user = self._create_user(email, password, **kwargs)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password, birthday=date(year=2000, month=1, day=1), sex="Male")
        user.is_staff, user.is_superuser, user.is_active = (True, True, True)
        user.save(using=self._db)
        return user


class SexSelection(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")


class User(AbstractUser):
    """Account model"""
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None
    email = fields.EmailField(_("Email address"))
    password = fields.PasswordField(_("Password"), max_length=128)
    last_login = models.DateTimeField(_("Last login"), blank=True, null=True, editable=False)
    date_joined = models.DateTimeField(_("Date joined"), default=timezone.now, editable=False)
    last_password_update = models.DateTimeField(_("Last password update"), blank=True, null=True, editable=False)
    last_email_received = models.DateTimeField(_("Last email received"), default=current_time_timedelta, editable=False)

    photo = models.ImageField(_("Photo profile"), null=True)
    first_name = fields.TitleCharField(_("First name"))
    last_name = fields.TitleCharField(_("Last name"))
    birthday = fields.BirthdayField(_("Birthday"))
    sex = fields.TitleCharField(_("Sex"), choices=SexSelection.choices)

    def __str__(self):
        return f'{self.email}'

    def set_password(self, raw_password):
        """Setting encrypted password with update last_password_update field"""
        super().set_password(raw_password)
        self.last_password_update = timezone.now()

    def email_user(self, subject: str, message: str, from_email=None, **kwargs) -> "send_email_celery":
        """async sending email for user by rewriting the original function"""
        kwargs['subject'] = subject
        kwargs['message'] = message
        kwargs['from_email'] = from_email
        kwargs['recipient_list'] = [self.email]
        return celery_current_app.send_task('celery_async_send_email', (), kwargs)

    def refresh_access_token(self) -> Token:
        """refresh access token and update refresh token"""
        return RefreshToken.for_user(self)

    def activate_account(self, token: str):
        """Activating email by token from DRF and return access token with refresh token"""
        if self.is_active is False and check_token(self, token):
            self.is_active = True
            self.save()

    def send_confirm_email(self) -> "send_email_celery":
        """Send email to confirm ownership"""
        subject = _('{} Confirm email ownership').format(settings.PROJECT_NAME)
        context = get_context(self, "https://{frontend}/account/confirm?uid={uid}&token={token}")
        html_message = render_to_string('accounts/email_confirm.html', context)
        return self.email_user(subject, '', html_message=html_message)

    def send_reset_password(self) -> "send_email_celery":
        """Send email to reset password"""
        subject = _('{} Reset your password').format(settings.PROJECT_NAME)
        context = get_context(self, "https://{frontend}/account/reset-password?uid={uid}&token={token}")
        html_message = render_to_string('accounts/reset_password.html', context)
        self.last_email_received = timezone.now()
        self.save()
        return self.email_user(subject, '', html_message=html_message)
