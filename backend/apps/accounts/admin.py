
from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    search_fields = ('email', 'first_name', 'last_name', 'birthday')
    search_help_text = "Search fields: email, name, surname, birthday"

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ()
        return ('password',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return 'email', 'last_login', 'date_joined', 'latest_token_update'

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return (("Creation", {'fields': ('email', 'password', 'first_name', 'last_name', 'birthday', 'sex')}),)
        return [("Editing", {"fields": self.get_fields(request, obj)})]

    def save_model(self, request, obj, form, change):
        if not change:
            models.User.objects.create_user(**form.cleaned_data)
        super().save_model(request, obj, form, change)
