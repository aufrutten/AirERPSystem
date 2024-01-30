from datetime import timedelta
from typing import TYPE_CHECKING

from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

import social_core.exceptions
from social_django.utils import psa

from rest_framework import serializers


if TYPE_CHECKING:
    from .models import User


@psa()
def register_by_access_token(request, backend) -> "User":
    try:
        token = request.data.get('provider_token')
        return request.backend.do_auth(token)
    except social_core.exceptions.AuthForbidden as error:
        raise serializers.ValidationError(error)


def current_time_timedelta():
    """Return the (current time - timedelta in hours, minutes, and...)"""
    return timezone.now() - timedelta(hours=1)


def check_last_email_received(user: "User") -> bool:
    """True if available to send new email else False. Antispam function. Delay between emails."""
    return timezone.now() - user.last_email_received >= timedelta(hours=1)


def get_token(user: "User") -> str:
    """Generate each time an access token for the given user"""
    return default_token_generator.make_token(user)


def check_token(user: "User", token: str) -> bool:
    """Check that the token is valid for the given user"""
    return default_token_generator.check_token(user, token)


def get_context(user: "User", url: str) -> dict:
    return {
        "user": user,
        "HOSTS": settings.HOSTS,
        "PROJECT_NAME": settings.PROJECT_NAME,
        "url": url.format(
            frontend=settings.HOSTS.frontend,
            uid=urlsafe_base64_encode(force_bytes(user.pk)),
            token=get_token(user)
        ),
    }
