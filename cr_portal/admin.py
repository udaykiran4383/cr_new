from django.contrib import admin
from . models import UserProfile , Leaderboard , Invite , Team, Blog
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class UserProfileAdmin(ImportExportModelAdmin):
    search_fields=('name','cr_id','ref',)

class TeamAdmin(ImportExportModelAdmin):
    search_fields=('teamname','leader','crid1','member2','crid2','member3','crid3','member4','crid4')

class NewTeamAdmin(ImportExportModelAdmin):
    list_display = ('teamname','leader','crid1','member2','crid2','member3','crid3','member4','crid4')


#@admin.register(UserProfile,Leaderboard,Invite,Team,Blog)
#class ViewAdmin(ImportExportModelAdmin):
#    pass


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Leaderboard)
admin.site.register(Invite)
admin.site.register(Team,TeamAdmin)
admin.site.register(Blog)


