from django.utils.translation import gettext as _

from rest_framework import serializers

from .serializers import EmailSerializer, AccessTokenSerializer


class LogoutSerializer(serializers.Serializer):
    pass


class LoginSerializer(EmailSerializer, AccessTokenSerializer):
    password = serializers.CharField(label=_('Password'), write_only=True)

    def validate_password(self, value: str) -> str:
        """check password for the user"""
        if self.instance and self.instance.check_password(value):
            return value
        raise serializers.ValidationError(_("The password you provided is incorrect"))
