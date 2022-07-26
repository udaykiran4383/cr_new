from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('signup',views.signup,name="signup"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('profile',views.profile,name="profile"),
    path('updateprofile',views.updateprofile,name="updateprofile"),
    path('invite/<int:id>',views.invite,name='invite'),
    path('point/<int:id>',views.point,name='point'),
    path('accept/<int:id>/<int:sender_id>',views.accept,name='accept'),
    path('confirm',views.confirm,name="confirm"),
    path('task1',views.task1,name="task1"),
    path('leaderboard',views.leaderboard,name="leaderboard"),
    path('teamLeaderboard', views.teamLeaderboard,name="teamLeaderboard"),
    path('team', views.team, name="team"),
    # path('cpanel',views.cpanel,name="cpanel"),

]
