# urls.py
from django.urls import path
from .views import AssignTask, home

app_name = 'kanban'

urlpatterns = [
    path('home/', home, name='home'),
    path('job-assign/<str:emp_id>/<str:task_id>/',
         AssignTask.as_view(), name='change_sheet_assign')
]
# there isn't full path in urlpatterns, the 'myapp/' is missing.
# This is app prefix, configured in main urls.py file
# ... path('myapp/', include('myapp.urls')), ...
