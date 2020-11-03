from django.contrib import admin
from .models import RasioKeuangan
from import_export.admin import ImportExportModelAdmin

@admin.register(RasioKeuangan)
class RasioKeuanganAdmin(ImportExportModelAdmin):
    pass