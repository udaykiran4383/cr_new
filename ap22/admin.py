from django.contrib import admin

from .models import Student , Team, Mentor, Playbook, D2c

from import_export.admin import ImportExportModelAdmin


# Register your models here.
#admin.site.register(Student)
#admin.site.register(Team)
#admin.site.register(Mentor)
#admin.site.register(Playbook)
#admin.site.register(D2c)

@admin.register(Team,Mentor,Playbook,D2c)
class ViewAdmin(ImportExportModelAdmin):
    pass
