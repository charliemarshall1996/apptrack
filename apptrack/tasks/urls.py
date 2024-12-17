
from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('task-cards/', views.task_cards_view, name='task_cards'),
    path('task-update/<int:id>/', views.task_update_view, name='update_task'),
]
