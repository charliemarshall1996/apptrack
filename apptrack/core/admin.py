from django.contrib import admin
from django.apps import apps

app_models = apps.get_app_config("core").get_models()

# Register all models
for model in app_models:
    admin.site.register(model)
