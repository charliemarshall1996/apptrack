
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Profile
from accounts.views import user_login
from .models import Target


@receiver(post_save, sender=Profile)
def create_target(sender, instance, created, **kwargs):
    existing_target = Target.objects.filter(profile=instance).first()

    if created or not existing_target:
        Target.objects.create(profile=instance)


@receiver(user_login)
def save_target(sender, user, **kwargs):
    profile = user.profile

    target, created = Target.objects.get_or_create(profile=profile)
    target.save()
