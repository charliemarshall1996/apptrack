# noqa: D100
from django.urls import path
from . import views
app_name = "jobs"

urlpatterns = [
    path("add/", views.job_add_view, name="add"),
    path("archive/", views.JobArchiveView.as_view(), name="archive"),
    path("delete/<int:pk>/", views.JobDeleteView.as_view(), name="delete"),
    path("download/", views.job_download_view, name="download"),
    path("edit/<int:pk>/", views.job_edit_view, name="edit"),
    path("list/", views.JobListView.as_view(), name="list"),
    path("settings/", views.settings_view, name="settings"),
]
