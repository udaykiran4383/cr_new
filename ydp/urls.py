from django.urls import path ,include
from . import views as ydp_views

urlpatterns = [
    path("Google", ydp_views.GoogleUser_list, name="Google"),
    path("Normal", ydp_views.NormalUser_list, name="Normal"),
]
