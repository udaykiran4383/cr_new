from django.contrib import admin
from . models import UserProfile , Leaderboard , Invite , Team
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Leaderboard)
admin.site.register(Invite)
admin.site.register(Team)