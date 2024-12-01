
from django.urls import path
from . import views

app_name = 'interview'
urlpatterns = [
    path("calendar/", views.calendar, name="calendar"),
    path("add-interview/", views.add_interview, name="add_interview"),
    path('detail/<int:interview_id>/',
         views.interview_detail, name='interview_detail'),
]
