
from django.urls import path
from . import views

app_name = 'interview'
urlpatterns = [
    path("calendar/", views.calendar, name="calendar"),
    path("add-interview/", views.add_interview, name="add_interview"),
    path('event-detail/<int:interview_id>/',
         views.interview_event_detail, name='interview_event_detail'),
]
