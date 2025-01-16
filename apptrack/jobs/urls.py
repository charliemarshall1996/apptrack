# noqa: D100
from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("board/", views.board_view, name="board"),
    path("add/", views.job_add_view, name="add"),
    path("archive/", views.JobArchiveView.as_view(), name="archive"),
    path(
        "assign/<str:col_id>/<str:job_id>/",
        views.JobAssignView.as_view(),
        name="assign",
    ),
    path("delete/<int:pk>/", views.JobDeleteView.as_view(), name="delete"),
    path("download/", views.job_download_view, name="download"),
    path("edit/<int:pk>/", views.job_edit_view, name="edit"),
    path("list/", views.JobListView.as_view(), name="list"),
]
