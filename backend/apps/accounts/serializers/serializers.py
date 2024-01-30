from typing import TYPE_CHECKING

from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from ..utils import check_token, check_last_email_received


if TYPE_CHECKING:
    from ..models import User
    from rest_framework_simplejwt.tokens import Token


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_('Email address'))

    def validate_email(self, value: str):
        """check email for existing and activating"""
        self.instance: "User" = get_user_model().objects.filter(email=value.lower().strip()).first()

        if not self.instance:
            raise serializers.ValidationError(_("Unfortunately, the email address you provided was not found"))

        if not self.instance.is_active:
            raise serializers.ValidationError(_("Account is not yet activated, please confirm your email"))

        return value.lower().strip()


class EmailAntiSpamSerializer(EmailSerializer):

    def validate_email(self, value: str):
        value = super().validate_email(value)

        if not check_last_email_received(self.instance):
            raise serializers.ValidationError(
                _("Cannot send reset link too frequently. "
                  "Check your email or wait before requesting another one.")
            )

        return value


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(label=_('Password'), max_length=128, write_only=True)

    def validate_password(self, value: str) -> str:
        """Password check for a match with the first and last name or email"""
        data = dict(self.get_initial())

        if "uid" in data:
            data["pk"] = force_str(urlsafe_base64_decode(data.pop("uid")))

        user: "User" = self.instance or get_user_model().objects.filter(**data).first() or get_user_model()(**data)
        validate_password(value.strip(), user)

        return value.strip()


class UIDSerializer(serializers.Serializer):
    uid = serializers.CharField(label=_('User ID'), write_only=True)

    def validate_uid(self, value: str) -> str:
        """Check user ID"""
        try:
            uid = force_str(urlsafe_base64_decode(value))
            self.instance: "User" = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise serializers.ValidationError(_('Invalid user ID'))

        return value


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(label=_('Token'), write_only=True)

    def validate_token(self, value: str) -> str:
        """Check token for requested user"""
        if not check_token(self.instance, value):
            raise serializers.ValidationError(_('Invalid token'))

        return value


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.SerializerMethodField(label=_('Access token'), read_only=True)
    refresh_token = serializers.SerializerMethodField(label=_('Refresh token'), read_only=True)
    __refresh_token = None

    def get_access_token(self, value: str) -> str:
        self.__refresh_token: "Token" = self.instance.refresh_access_token()
        return str(self.__refresh_token.access_token)

    def get_refresh_token(self, value: str) -> str:
        return str(self.__refresh_token)
