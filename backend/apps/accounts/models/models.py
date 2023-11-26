
from datetime import date

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager

from celery import current_app as celery_current_app
from rest_framework_simplejwt.tokens import RefreshToken

from . import fields


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
        user.refresh_access_token()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password, birthday=date(year=2000, month=1, day=1), sex="Male")
        user.is_staff, user.is_superuser, user.is_active = (True, True, True)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    sex_selections = (("Male", _("Male")), ("Female", _("Female")))
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None
    email = fields.EmailField(_("Email address"))
    password = models.CharField(_("password"), max_length=128)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True, editable=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now, editable=False)

    photo = fields.CloudinaryField(_("Photo profile"))
    first_name = fields.TitleCharField(_("First name"))
    last_name = fields.TitleCharField(_("Last name"))
    birthday = fields.BirthdayField(_("Birthday"))
    sex = fields.TitleCharField(_("Sex"), choices=sex_selections)

    access_token = models.CharField(_("Access token"), max_length=256, editable=False)
    refresh_token = models.CharField(_("Refresh token"), max_length=256, editable=False)
    latest_token_update = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{self.email}'

    def email_user(self, subject, message, from_email=None, **kwargs):
        """async sending email for user by rewriting the original function"""
        kwargs['subject'] = subject
        kwargs['message'] = message
        kwargs['from_email'] = from_email
        kwargs['recipient_list'] = [self.email]
        celery_current_app.send_task('celery_async_send_email', (), kwargs)

    def refresh_access_token(self):
        """refresh access token and update refresh token"""
        refresh = RefreshToken.for_user(self)
        self.refresh_token, self.access_token = str(refresh), str(refresh.access_token)
        self.latest_token_update = timezone.now()
        self.save()

    def activate_account(self, access_token):
        if self.is_active is False and self.access_token == access_token:
            self.is_active = True
            self.refresh_access_token()
