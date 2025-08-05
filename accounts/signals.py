from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

# Assuming this is a custom signal, not a view
from core.choices import StatusChoices

from . import models, views


@receiver(post_save, sender=models.CustomUser)
def create_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.get_or_create(user=instance)


@receiver(views.login.user_login)
def create_profile_on_user_login(sender, instance, **kwargs):
    models.Profile.objects.get_or_create(user=instance)
