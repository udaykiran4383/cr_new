from django.urls import path ,include
from . import views as apviews

urlpatterns = [
    path("student", apviews.students_list, name="student"),
    path("team", apviews.teams_list, name="team"),
    path("login", apviews.login_view, name="login"),
    path("mentor", apviews.mentors_list, name="mentor"),
    path("playbook", apviews.playbooks_list, name="playbook"),
    path('newteam', apviews.simple_upload),

    # path("mail" , views.apmail,name="apmail")
    # path('auth/',include('drf_social_oauth2.urls',namespace='drf'))
]
