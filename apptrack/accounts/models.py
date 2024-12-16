
import logging

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import Signal
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager
# Create your models here.

target_reset = Signal()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model that uses email instead of username."""

    email = models.EmailField(_('email address'), unique=True)
    email_verified = models.BooleanField(default=False)

    last_verification_email_sent = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email instead of username for authentication
    # These fields will be prompted in createsuperuser
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Profile(models.Model):

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile', unique=True)
    email_comms_opt_in = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    current_applications_made = models.IntegerField(
        null=True, blank=True, default=0)
    last_reset = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


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
    amount = models.IntegerField(default=0, null=True, blank=True)
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

    def _reset_if_target_changed(self):
        try:
            Target.objects.get(pk=self.pk)
            original = Target.objects.get(pk=self.pk)
            if original.amount != self.amount:
                self.current = 0
                self.last_reset = timezone.now()
                target_reset.send(sender=self.__class__, instance=self)
        except Target.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        self._reset_if_target_changed()
        self.reset(from_save=True)
        super().save(*args, **kwargs)
