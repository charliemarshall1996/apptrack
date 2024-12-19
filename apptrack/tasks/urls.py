from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [path("cards/", views.task_cards_view, name="cards")]
