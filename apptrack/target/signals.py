import logging

from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile
from accounts.views import user_login
from .models import Target
from .views import target_reset

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def create_target_on_profile_creation(sender, instance, created, **kwargs):
    logger.info("Profile created: %s", instance)
    if created:
        logger.debug("Profile is new. Creating target...")
        Target.objects.create(profile=instance, amount=5)
        logger.debug("Target created")


@receiver(user_login)
def save_target_on_login(sender, user, **kwargs):
    profile = Profile.objects.get(user=user)

    try:
        target, created = Target.objects.get_or_create(profile=profile)
    except MultipleObjectsReturned:
        target = Target.objects.filter(profile=profile).first()
    except Target.DoesNotExist:
        target = Target(profile=profile)
        target.save()
    target.save()


@receiver(target_reset)
def reset_target(sender, profile, **kwargs):
    target = Target.objects.get(profile=profile)
    target.current = 0
    target.streak.current_streak = 0
    target.streak.save()
    target.save()
