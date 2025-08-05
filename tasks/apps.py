"""Tasks apps setup."""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Tasks app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks"
