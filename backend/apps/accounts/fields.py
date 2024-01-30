__all__ = ('EmailField', 'BirthdayField', 'TitleCharField', 'PasswordField')

from django.db import models

from . import validators


class EmailField(models.EmailField):
    default_validators = [validators.validate_email] + models.EmailField.default_validators.copy()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('unique', True)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value: str = getattr(model_instance, self.attname)
        if value is not None:
            value = value.strip().lower()
        setattr(model_instance, self.attname, value)
        return value


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
        value: str = getattr(model_instance, self.attname)
        if value is not None:
            value = value.title().strip()
        setattr(model_instance, self.attname, value)
        return value


class PasswordField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 128)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value: str = getattr(model_instance, self.attname)
        if value is not None:
            value = value.strip()
        setattr(model_instance, self.attname, value)
        return value
