from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
  path("jobs-list/", views.JobsListView.as_view(), name="jobs_list"),
  path("add-job/", views.add_job_view, name="add_job"),
  path("update-job/<int:pk>/", views.update_job_view, name="update_job"),
]