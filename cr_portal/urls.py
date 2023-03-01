from unicodedata import name
from django.urls import path
from . import views as crview

urlpatterns = [
    path('',crview.index, name="index"),
    path('login',crview.login,name="login"),
    path('logout',crview.logout,name="logout"),
    path('signup',crview.signup,name="signup"),
    path('dashboard/<int:id>',crview.dashboard,name="dashboard"),
    path('updateprofile/<int:id>',crview.updateprofile,name="updateprofile"),
    path('myprofile/<int:id>',crview.myprofile ,name="myprofile"),
    path('invite/<int:id>',crview.invite,name='invite'),
    path('point/<int:id>',crview.point,name='point'),
    path('accept/<int:id>/<str:cr>/<str:sender_id>',crview.accept,name='accept'),
    path('reject/<int:id>/<str:cr>/<str:sender_id>',crview.reject,name='reject'),
    path('task/<int:id>',crview.task,name="task"),
    path('task1/<int:id>',crview.task1,name="task1"),
    path('leaderboard/<int:id>',crview.leaderboard,name="leaderboard"),
    path('blog/<int:id>', crview.blog, name="blog"),
    path('yourprofile/<int:id>',crview.yourprofile, name="yourprofile"),
    path('sendagain/<int:id>/<str:cr>/<str:sender_id>',crview.sendagain, name="sendagain"),
    path('newinvite/<int:id>', crview.newinvite, name="newinvite"),
    path('team/<int:id>', crview.team, name="team"),
    path('export',crview.export,name="export"),
    path('teamexport',crview.teamexport,name="teamexport"),
    path('teamsort',crview.teamsort,name="teamsort"),
    path('google',crview.google,name="google"),
    path('ref_count',crview.ref_count,name="ref_count"),
    path('newteam', crview.simple_upload),
    path('taskmail',crview.taskmail,name="taskmail"),

]
