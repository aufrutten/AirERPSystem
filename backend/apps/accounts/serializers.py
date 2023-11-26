
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password

from . import utils


class AccountLogoutSerializer(serializers.Serializer):
    pass


class AccountLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_('Email address'))
    password = serializers.CharField(label=_('Password'), write_only=True)
    access_token = serializers.CharField(label=_('Access token'), read_only=True)
    refresh_token = serializers.CharField(label=_('Refresh token'), read_only=True)

    def validate_email(self, value: str) -> str:
        """check email for existing and activating"""
        self.instance = get_user_model().objects.filter(email=value.lower()).first()
        if self.instance:
            if self.instance.is_active:
                return value.lower()
            raise serializers.ValidationError(_("Account is not yet activated, please confirm your email"))
        raise serializers.ValidationError(_("Unfortunately, the email address you provided was not found"))

    def validate_password(self, value: str) -> str:
        """check password for the user"""
        data = dict(self.get_initial())
        if authenticate(email=data.get('email'), password=value):
            return value
        raise serializers.ValidationError(_("The password you provided is incorrect"))

    def get_response(self):
        self.is_valid(raise_exception=True)
        response = self.data
        response['access_token'] = self.instance.access_token
        response['refresh_token'] = self.instance.refresh_token
        return response


class CreateAccountSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(allow_null=True, required=False)
    password = serializers.CharField(label=_("Password"), max_length=128, write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ['photo', 'first_name', 'last_name', 'birthday', 'sex', 'email', 'password']

    def validate_password(self, value):
        """Password check for a match with the first and last name or email"""
        user = self.instance or self.Meta.model(**dict(self.get_initial()))
        validate_password(value, user)
        return value

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        user.email_user(**utils.RenderEmail(user, choice='confirm')())
        return user


class AccountSerializer(CreateAccountSerializer):

    class Meta(CreateAccountSerializer.Meta):
        fields = CreateAccountSerializer.Meta.fields.copy()
        fields += ['last_login', 'date_joined', 'access_token', 'refresh_token', 'latest_token_update']

        read_only_fields = ['sex', 'email', 'birthday', 'last_login', 'date_joined']
        read_only_fields += ['refresh_token', 'latest_token_update', 'access_token']

    def validate_access_token(self, value: str) -> str:
        if self.instance and value == self.instance.access_token:
            return value
        raise serializers.ValidationError(_('The token you provided is incorrect'))

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
            del validated_data['password']
        return super().update(instance, validated_data)


class AccountConfirmSerializer(AccountSerializer, AccountLoginSerializer):
    access_token = serializers.CharField(label=_('Access token'))

    class Meta(AccountSerializer.Meta):
        fields = ['email', 'access_token', 'refresh_token']
        read_only_fields = AccountSerializer.Meta.read_only_fields.copy()
        read_only_fields += ['refresh_token']

    def validate_email(self, value: str) -> str:
        """check email for existing and account is deactivated"""
        self.instance = get_user_model().objects.filter(email=value.lower()).first()
        if self.instance and self.instance.is_active is False:
            return value.lower()
        raise serializers.ValidationError(_("Unfortunately, the email address you provided was not found"))


class POSTAccountResetSerializer(AccountSerializer, AccountLoginSerializer):

    class Meta(AccountSerializer.Meta):
        fields = ['email']


class PUTAccountResetSerializer(AccountSerializer, AccountLoginSerializer):
    access_token = serializers.CharField(label=_('Access token'), write_only=True)

    class Meta(AccountSerializer.Meta):
        fields = ['email', 'access_token', 'password']


class POSTAccountSocialAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_('Email address'), read_only=True)
    access_token = serializers.CharField(label=_('Access token'), read_only=True)
    refresh_token = serializers.CharField(label=_('Refresh token'), read_only=True)

    provider_token = serializers.CharField(label=_('Access token'), required=True,
                                           write_only=True, help_text=_('Access token from provider'))


class GETAccountSocialAuthSerializer(serializers.Serializer):
    client_id = serializers.CharField(label=_('Client id'), read_only=True, help_text=_('Client id of app'))
