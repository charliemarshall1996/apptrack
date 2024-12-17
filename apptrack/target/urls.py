
from django.urls import path
from . import views

app_name = "targets"

urlpatterns = [
    path("update/", views.target_update_view, name="update_target")
]
