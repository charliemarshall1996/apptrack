from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.apps import apps

# Get all models from the 'core' app
app_models = apps.get_app_config('accounts').get_models()

# Register all models
for model in app_models:
    admin.site.register(model)