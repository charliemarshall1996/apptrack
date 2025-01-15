from django.urls import path
from . import views

app_name = "interviews"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("interview-add/", views.interview_add_view, name="add_interview"),
    path()
]
