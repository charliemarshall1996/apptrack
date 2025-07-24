"""Tasks apps setup."""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Tasks app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks"

    def ready(self):
        """Tasks app ready method. Enables signals."""
        import tasks.signals  # noqa
