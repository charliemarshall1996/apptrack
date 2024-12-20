"""Signals for the target app.

This module contains the signals for the target app. create_target_on_profile_creation
is called when a new profile is created, creating a corresponding target for the profile
instance. save_target_on_login is called when a user logs in.
"""

import logging

from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile
from accounts.views import user_login
from .models import Target

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def create_target_on_profile_creation(sender, instance, created, **kwargs):
    """Creates a target for a new profile.

    This signal handler is triggered when a new profile is created. It creates a
    new target instance associated with the profile and sets the default target amount
    to 5.

    Args:
        sender (Model): The model class that sent the signal.
        instance (Profile): The instance of the profile that was saved.
        created (bool): A boolean indicating if a new record was created.
        **kwargs (dict): Additional keyword arguments.
    """
    logger.info("Profile created: %s", instance)
    if created:
        logger.debug("Profile is new. Creating target...")
        Target.objects.create(profile=instance, amount=5)
        logger.debug("Target created")


@receiver(user_login)
def save_target_on_login(sender, user, **kwargs):
    """Saves the target for a user when they log in.

    This signal handler is triggered when a user logs in. It gets the target associated
    with the user's profile and saves it. If the target does not exist, it creates one.
    If multiple targets exist, it uses the first one. Finally, it saves the target.

    Args:
        sender (Model): The model class that sent the signal.
        user (User): The user who logged in.
        **kwargs (dict): Additional keyword arguments.
    """
    profile = Profile.objects.get(user=user)

    try:
        target, created = Target.objects.get_or_create(profile=profile)
    except MultipleObjectsReturned:
        target = Target.objects.filter(profile=profile).first()
    except Target.DoesNotExist:
        target = Target(profile=profile)
    finally:
        target.save()
