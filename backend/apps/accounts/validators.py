from datetime import date
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


def validate_email(value: str) -> str:
    """Controlling if email available for use, is not busy"""
    if get_user_model().objects.filter(email=value.lower().strip()).exists():
        raise ValidationError(_("Sorry, but this email address is already linked to another account."))
    return value.lower().strip()


def validate_birthday(value):
    """Check if person not under or upper the age which below in settings"""
    diff = relativedelta(date.today(), value)
    min_age, max_age = settings.AGE_REMARK["MIN"], settings.AGE_REMARK["MAX"]
    if diff.years < settings.AGE_REMARK["MIN"]:  # if person under <18
        raise ValidationError(_('Your age is below the minimum required {} year olds.').format(min_age))
    if diff.years >= settings.AGE_REMARK["MAX"]:  # if person upper >65
        raise ValidationError(_('Sorry, but you need to be under the age of {} year olds.').format(max_age))
    return value
