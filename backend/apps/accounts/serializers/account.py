from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from .serializers import (
    PasswordSerializer,
    UIDSerializer,
    TokenSerializer,
    AccessTokenSerializer,
    EmailAntiSpamSerializer,
)


# =========================================ACCOUNT======================================================================

class CreateAccountSerializer(serializers.ModelSerializer, PasswordSerializer):

    class Meta:
        model = get_user_model()
        fields = ['photo', 'first_name', 'last_name', 'birthday', 'sex', 'email', 'password']

    def create(self, validated_data):
        """Create the account and send him the email confirm"""
        user = self.Meta.model.objects.create_user(**validated_data)
        user.send_confirm_email()
        return user


class AccountSerializer(CreateAccountSerializer):
    password = serializers.CharField(label=_('Password'), max_length=128, write_only=True, required=False)

    class Meta(CreateAccountSerializer.Meta):
        fields = CreateAccountSerializer.Meta.fields.copy()
        fields += ['last_login', 'date_joined', 'last_password_update']
        read_only_fields = ['sex', 'email', 'birthday', 'last_login', 'date_joined', 'last_password_update']

    def update(self, instance, validated_data):
        """update account fields and set password by crypt func"""
        if validated_data.get('password'):
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)


class ForgotPasswordSerializer(EmailAntiSpamSerializer):

    def save(self, **kwargs):
        """Send the email to reset password"""
        self.instance.send_reset_password()


class ChangePasswordSerializer(UIDSerializer, TokenSerializer, PasswordSerializer):

    def save(self):
        """Save the new password"""
        self.instance.set_password(self.validated_data['password'])
        self.instance.save()


class ConfirmEmailSerializer(UIDSerializer, TokenSerializer, AccessTokenSerializer):

    def save(self, **kwargs):
        """Activate account"""
        self.instance.activate_account(self.validated_data['token'])
        self.instance.save()
