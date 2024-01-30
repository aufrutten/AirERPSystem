from typing import TYPE_CHECKING

from django.conf import settings
from django.utils.translation import gettext as _

from rest_framework import serializers

from .serializers import AccessTokenSerializer
from ..utils import register_by_access_token


if TYPE_CHECKING:
    from ..models import User


class PUTSerializer(AccessTokenSerializer):
    email = serializers.EmailField(label=_('Email address'), read_only=True)
    provider_token = serializers.CharField(label=_('Access token'), required=True,
                                           write_only=True, help_text=_('Access token from social provider'))

    def validate_provider_token(self, value: str) -> str:
        request = self.context.get('request')
        social_backend = self.context.get('social_backend')

        if social_backend not in settings.AVAILABLE_OAUTH_BACKENDS_IN_API:
            raise serializers.ValidationError("OAuth isn't exist")

        self.instance: "User" = register_by_access_token(request, social_backend)
        return value


class GETSerializer(serializers.Serializer):
    client_id = serializers.SerializerMethodField(label=_('Client id'), read_only=True, help_text=_('Client id of app'))

    def get_client_id(self, value: str) -> str:
        social_backend = self.context.get('social_backend')

        if social_backend == 'all':
            return settings.AVAILABLE_OAUTH_BACKENDS_IN_API

        if social_backend in settings.AVAILABLE_OAUTH_BACKENDS_IN_API:
            return settings.AVAILABLE_OAUTH_BACKENDS_IN_API[social_backend]

        raise serializers.ValidationError("OAuth isn't exist")
