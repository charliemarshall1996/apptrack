from django.contrib import admin
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name="home"),
    # path('test-api', views.get_data),
    path('api/', views.ChartData.as_view()),
    path('basic-stats/<int:id>/',
         views.BasicStats.as_view()),
    path("job-source-conversion/<int:id>/",
         views.BestConvertingJobFunctions.as_view()),
    path("job-function-conversion/<int:id>/",
         views.BestConvertingJobFunctions.as_view()),
]
