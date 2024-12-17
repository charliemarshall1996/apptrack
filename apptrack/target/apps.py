from django.apps import AppConfig


class TargetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'target'

    def ready(self):
        import target.signals
