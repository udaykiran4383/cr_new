from unicodedata import name
from django.urls import path
from . import views as crview

urlpatterns = [
    path('',crview.index, name="index"),
    path('login',crview.login,name="login"),
    path('logout',crview.logout,name="logout"),
    path('signup',crview.signup,name="signup"),
    path('dashboard',crview.dashboard,name="dashboard"),
    path('profile',crview.profile,name="profile"),
    path('updateprofile',crview.updateprofile,name="updateprofile"),
    path('invite/<int:id>',crview.invite,name='invite'),
    path('point/<int:id>',crview.point,name='point'),
    path('accept/<int:id>/<int:cr>/<int:sender_id>',crview.accept,name='accept'),
    path('confirm',crview.confirm,name="confirm"),
    path('task1',crview.task1,name="task1"),
    path('leaderboard',crview.leaderboard,name="leaderboard"),
    path('blog', crview.blog, name="blog"),
    # path('teamLeaderboard', crview.teamLeaderboard,name="teamLeaderboard"),
    path('team', crview.team, name="team"),
    # path('cpanel',views.cpanel,name="cpanel"),

]
