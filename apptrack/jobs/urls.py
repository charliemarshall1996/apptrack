from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'jobs'

urlpatterns = [
    # Route to display the Kanban board
    path('board/', views.board_view, name='board'),

    # Route to handle job assignment (moving jobs between columns via AJAX)
    path('job-assign/<str:col_id>/<str:job_id>/',
         views.AssignJobView.as_view(), name='assign_job'),

    # Any other views, like adding or updating jobs
    path("add-job/", views.add_job_view, name="add_job"),
    path("update-job/<int:pk>/", views.update_job_view, name="update_job"),
]
