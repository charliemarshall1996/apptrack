"""URLs for the target app."""

from django.urls import path
from . import views

app_name = "target"

urlpatterns = [path("update/", views.target_update_view, name="update")]
