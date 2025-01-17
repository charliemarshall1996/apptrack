from django.contrib import admin
from django.apps import apps

app_models = apps.get_app_config("blog").get_models()

for model in app_models:
    admin.site.register(model)
