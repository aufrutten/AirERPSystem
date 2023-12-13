
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from . import models


@admin.register(models.Airport)
class AirportAdmin(ImportExportModelAdmin):
    search_fields = ('name', 'municipality', 'iata_code', 'keywords', 'id')

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return ('last_update',)

