
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile
from .models import Target


@receiver(post_save, sender=Profile)
def create_target(sender, instance, created, **kwargs):
    existing_target = Target.objects.filter(profile=instance).first()

    if created or not existing_target:
        Target.objects.create(profile=instance)
