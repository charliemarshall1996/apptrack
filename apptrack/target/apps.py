"""Target app setup.

This module contains the setup for the target app. 
TargetConfig is the app config class. It enables signals.
"""
from django.apps import AppConfig


class TargetsConfig(AppConfig):
    """Target app configuration.

    Attributes:
        default_auto_field (str): The default auto field for the app.
        name (str): The name of the app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "target"

    def ready(self):
        """Enables signals for the target app.

        The ready method is called by Django as soon as the registry is fully populated.
        It enables signals for the target app. The signals are defined in 
        target.signals.
        """
        import target.signals  # noqa
