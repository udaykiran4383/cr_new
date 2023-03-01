from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import GoogleUser, NormalUser
# Register your models here.

@admin.register(GoogleUser,NormalUser)
class ViewAdmin(ImportExportModelAdmin):
    pass
