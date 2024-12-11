from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('board/', views.board_view, name='board'),
    path('job-assign/<str:col_id>/<str:job_id>/',
         views.AssignJobView.as_view(), name='assign_job'),
    path("add-job/", views.add_job_view, name="add_job"),
    path("edit-job/<int:pk>/", views.edit_job_view, name="edit_job"),
    path("delete-job/<int:pk>/", views.DeleteJobView.as_view(), name="delete_job"),
    path("download", views.download_jobs_view, name="download"),
    path("list", views.JobListView.as_view(), name="list"),
    path("archive/", views.ArchiveJobView.as_view(), name="archive_job"),

    path("calendar/", views.calendar, name="calendar"),
    path("add-interview/", views.add_interview, name="add_interview"),
    path('event-detail/<int:interview_id>/',
         views.interview_event_detail, name='interview_event_detail'),
    path('edit-interview/<int:interview_id>/',
         views.edit_interview, name='edit_interview'),
    path('update-task/<int:id>/', views.update_task, name='update_task'),
]
