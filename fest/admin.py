from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import GoogleUser, NormalUser, Event, ConvoUser
# Register your models here.

@admin.register(GoogleUser,NormalUser, Event,ConvoUser)
class ViewAdmin(ImportExportModelAdmin):
    pass


