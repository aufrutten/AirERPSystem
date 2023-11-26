
__all__ = ('CloudinaryField', 'EmailField', 'BirthdayField', 'TitleCharField')


from django.db import models
from cloudinary.models import CloudinaryField as RawCloudField
from . import validators


class CloudinaryField(RawCloudField):

    def __init__(self, *args, **kwargs):
        self.url = None
        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)


class EmailField(models.EmailField):
    default_validators = [validators.validate_email] + models.EmailField.default_validators.copy()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('unique', True)
        kwargs.setdefault('max_length', 256)
        super().__init__(*args, **kwargs)


class BirthdayField(models.DateField):
    default_validators = [validators.validate_birthday] + models.DateField.default_validators.copy()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('null', False)
        kwargs.setdefault('blank', False)
        super().__init__(*args, **kwargs)


class TitleCharField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("null", False)
        kwargs.setdefault("blank", False)
        kwargs.setdefault("max_length", 150)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = model_instance.__dict__[self.name]
        if value is not None:
            value = value.title()
        model_instance.__dict__[self.name] = value
        return value
