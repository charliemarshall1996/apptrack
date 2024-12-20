"""Models for the target app.

The target model stores information about the target number of daily applications made
for the corresponding profile's user. The streak model stores information about the
current and longest streak for the corresponding target models profile's user.
"""

import logging

from django.db import models
from django.dispatch import Signal
from django.utils import timezone

from accounts.models import Profile
# Create your models here.

logger = logging.getLogger(__name__)

target_reset = Signal()


class Streak(models.Model):
    """Streak data for a users target number of daily applications made.

    The streak model stores information about the current and longest streak for the
    corresponding profile's user.

    Attributes:
        current_streak_start (models.DateTimeField):
            The start date of the current streak for the corresponding profile.
        current_streak (models.IntegerField):
            The current value of the streak for the corresponding profile.
        longest_streak_start (models.DateTimeField):
            The start date of the longest streak for the corresponding profile.
        longest_streak_end (models.DateTimeField):
            The end date of the longest streak for the corresponding profile.
        longest_streak (models.IntegerField):
            The longest value of the streak for the corresponding profile.
    """

    current_streak_start = models.DateTimeField(
        null=True, blank=True, auto_now_add=True
    )
    current_streak = models.IntegerField(default=0, null=True, blank=True)

    longest_streak_start = models.DateTimeField(null=True, blank=True)
    longest_streak_end = models.DateTimeField(null=True, blank=True)
    longest_streak = models.IntegerField(default=0, null=True, blank=True)

    def increment(self):
        """Increments the current_streak by 1.

        This method increments the current_streak by 1 and saves the instance.
        """
        self.current_streak += 1
        self.save()

    def reset(self):
        """Resets the current streak to 0 and updates the longest streak if necessary.

        This method compares the current streak to the longest streak. If the current
        streak is greater than the longest streak, the longest streak is updated with
        the current streak. It then resets the current streak to 0 and saves the
        instance.
        """
        now = timezone.now()
        if self.current_streak > self.longest_streak:
            self.longest_streak_start = self.current_streak_start
            self.longest_streak_end = now
            self.longest_streak = self.current_streak
        self.current_streak_start = now
        self.current_streak = 0
        self.save()


class Target(models.Model):
    """Target model.

    The target model stores information about the target number of daily applications
    made for the corresponding profile's user.

    Attributes:
        profile (models.OneToOneField):
            The profile associated with the target.
        amount (models.IntegerField):
            The target amount for the corresponding profile.
        current (models.IntegerField):
            The current value of the target for the corresponding profile.
        total_targets_met (models.IntegerField):
            The total number of times the target has been met for the corresponding
            profile.
        streak (models.ForeignKey):
            The streak associated with the target for the corresponding profile.
        last_reset (models.DateTimeField):
            The last time the target was reset for the corresponding profile.
    """

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="target", unique=True
    )
    amount = models.IntegerField(default=5, null=True, blank=True)
    current = models.IntegerField(default=0, null=True, blank=True)
    total_targets_met = models.IntegerField(default=0)
    streak = models.ForeignKey(
        Streak,
        on_delete=models.CASCADE,
        related_name="target",
        null=True,
        default=Streak.objects.create,
        unique=True,
    )
    last_reset = models.DateTimeField(auto_now_add=True)

    @property
    def met(self):
        """Checks if the target has been met.

        Returns:
            bool: True if the target has been met, False otherwise.
        """
        return self.current >= self.amount

    def reset(self, from_save=False):
        """Resets the amount property to 0.

        reset sends a signal to signal handlers that the target has been reset. If it
        has been met, the total_targets_met and streak.current_streak will be
        incremented. If it has not been met, the streak will be reset.

        Args:
            from_save (bool): If the method was called from the save method of the
                model, in which case the model should not be saved again.
        """
        now = timezone.now()

        logger.info("Starting reset. from_save: %s", from_save)

        if self.amount and self.last_reset:
            # if there is a target
            if self.amount > 0:
                logger.info("Amount is greater than 0. from_save: %s", from_save)
                if now.date() > self.last_reset.date():
                    logger.info("Date is different. from_save: %s", from_save)
                    logger.info("Different date")
                    if self.met:
                        logger.info("Target met. from_save: %s", from_save)
                        self.total_targets_met += 1
                        self.streak.increment()
                    else:
                        logger.info("Target not met. from_save: %s", from_save)
                        self.streak.reset()

                    self.current = 0
                    self.last_reset = now

                    logger.info("Checking if from save %s", from_save)
                    if not from_save:
                        logger.info("Calling save")
                        self.save()
                    else:
                        logger.info("Not calling save %s", from_save)

    def increment(self):
        """Increment the current value by 1 and save the Target instance."""
        self.current += 1
        self.save()

    def decrement(self):
        """Decrement the current value by 1 and save the Target instance."""
        self.current -= 1
        self.save()

    def save(self, *args, **kwargs):
        """Save method for Target.

        Calls the reset method to check if the target is met and to
        reset the target if it is not met or if the date has changed.

        Then calls the superclass's save method to persist the changes.
        """
        self.reset(from_save=True)
        super().save(*args, **kwargs)
