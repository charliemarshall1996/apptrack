
import logging

from django.db import models
from django.dispatch import Signal
from django.utils import timezone

from accounts.models import Profile
# Create your models here.

logger = logging.getLogger(__name__)

target_reset = Signal()


class Streak(models.Model):
    current_streak_start = models.DateTimeField(
        null=True, blank=True, auto_now_add=True)
    current_streak = models.IntegerField(default=0, null=True, blank=True)

    longest_streak_start = models.DateTimeField(null=True, blank=True)
    longest_streak_end = models.DateTimeField(null=True, blank=True)
    longest_streak = models.IntegerField(default=0, null=True, blank=True)

    def increment(self):
        self.current_streak += 1
        self.save()

    def reset(self):
        now = timezone.now()
        if self.current_streak > self.longest_streak:
            self.longest_streak_start = self.current_streak_start
            self.longest_streak_end = now
            self.longest_streak = self.current_streak
        self.current_streak_start = now
        self.current_streak = 0
        self.save()


class Target(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='target', unique=True)
    amount = models.IntegerField(default=5, null=True, blank=True)
    current = models.IntegerField(default=0, null=True, blank=True)
    total_targets_met = models.IntegerField(default=0)
    streak = models.ForeignKey(
        Streak, on_delete=models.CASCADE, related_name='target', null=True, default=Streak.objects.create, unique=True)
    last_reset = models.DateTimeField(auto_now_add=True)

    @property
    def met(self):
        return self.current >= self.amount

    def reset(self, from_save=False):
        # get now
        now = timezone.now()

        logger.info("Starting reset. from_save: %s", from_save)

        if self.amount and self.last_reset:
            # if there is a target
            if self.amount > 0:
                logger.info(
                    "Amount is greater than 0. from_save: %s", from_save)
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

                    logger.info("Sending signal. from_save: %s", from_save)
                    target_reset.send(sender=self.__class__, instance=self)

                    logger.info("Checking if from save %s", from_save)
                    if not from_save:
                        logger.info("Calling save")
                        self.save()
                    else:
                        logger.info("Not calling save %s", from_save)

    def increment(self):
        self.current += 1
        self.save()

    def decrement(self):
        self.current -= 1
        self.save()

    def save(self, *args, **kwargs):
        self.reset(from_save=True)
        super().save(*args, **kwargs)
