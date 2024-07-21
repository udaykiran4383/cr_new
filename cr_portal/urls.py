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



    path('yourprofile/<int:id>',crview.yourprofile, name="yourprofile"),
   

   
    path('google',crview.google,name="google"),
  
   
    path('taskmail',crview.taskmail,name="taskmail"),







]
