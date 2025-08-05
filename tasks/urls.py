"""URLs for the tasks app."""

from django import urls
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', views.TaskViewset, basename='tasks')
app_name = "tasks"

urlpatterns = router.urls
