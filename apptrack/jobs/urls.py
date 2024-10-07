from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Route to display the Kanban board
    path('board/', views.board_view, name='job_board'),

    # Route to handle job assignment (moving jobs between columns via AJAX)
    path('task-assign/<int:col_id>/<int:job_id>/',
         views.AssignTaskView.as_view(), name='assign_task'),

    # Any other views, like adding or updating jobs
    path("update-job/<int:pk>/", views.update_job_view, name="update_job"),
]
