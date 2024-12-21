# noqa: D100
from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("board/", views.board_view, name="board"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("interview-add/", views.interview_add_view, name="add_interview"),
    path(
        "interview-detail/<int:interview_id>/",
        views.interview_detail_view,
        name="interview_detail",
    ),
    path(
        "interview-edit/<int:interview_id>/",
        views.interview_edit_view,
        name="edit_interview",
    ),
    path("job-add/", views.job_add_view, name="add_job"),
    path("job-archive/", views.JobArchiveView.as_view(), name="archive_job"),
    path(
        "job-assign/<str:col_id>/<str:job_id>/",
        views.JobAssignView.as_view(),
        name="assign_job",
    ),
    path("job-delete/<int:pk>/", views.JobDeleteView.as_view(), name="delete_job"),
    path("job-download/", views.job_download_view, name="download_job"),
    path("job-edit/<int:pk>/", views.job_edit_view, name="edit_job"),
    path("job-list/", views.JobListView.as_view(), name="list"),
]
