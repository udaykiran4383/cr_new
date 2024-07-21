from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import UserProfile, Student, College

class UserProfileAdmin(ImportExportModelAdmin):
    search_fields = ('name', 'cr_id', 'ref')

admin.site.register(UserProfile, UserProfileAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'district', 'college')
    search_fields = ('name', 'state', 'district')

admin.site.register(Student, StudentAdmin)

class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'state')
    search_fields = ('name', 'district', 'state')

admin.site.register(College, CollegeAdmin)
