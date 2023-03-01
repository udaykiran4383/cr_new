from django.urls import path ,include
from . import views as ydp_views

urlpatterns = [
    path("Google", ydp_views.GoogleUser_list, name="Google"),
    path("Normal", ydp_views.NormalUser_list, name="Normal"),
    path("Event", ydp_views.Event_list, name="Event"),
    path("Event_reg", ydp_views.Event_reg, name="Event_reg"),
    path("Convo", ydp_views.ConvoUser_list, name="Convo"),

]

