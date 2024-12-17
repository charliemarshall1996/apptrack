
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile
from accounts.views import user_login
from .models import Target


@receiver(post_save, sender=Profile)
def create_target_on_profile_creation(sender, instance, created, **kwargs):

    if created:
        Target.objects.create(profile=instance, amount=5)


@receiver(user_login)
def save_target_on_login(sender, user, **kwargs):
    profile = Profile.objects.get(user=user)

    try:
        target, created = Target.objects.get_or_create(profile=profile)
    except MultipleObjectsReturned:
        target = Target.objects.filter(profile=profile).first()
    target.save()