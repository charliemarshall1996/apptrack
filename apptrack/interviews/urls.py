from django.urls import path
from . import views

app_name = "interviews"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("add/", views.add_view, name="add"),
    path(
        "detail/<int:interview_id>/",
        views.detail_view,
        name="detail",
    ),
    path(
        "edit/<int:interview_id>/",
        views.edit_view,
        name="edit",
    ),
]
