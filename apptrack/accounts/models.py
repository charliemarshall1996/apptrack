from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager
# Create your models here.


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


class Target(models.Model):
    WEEKLY = 'WK'
    DAILY = 'DA'
    UNIT_CHOICES = [
        (WEEKLY, "Weekly"),
        (DAILY, "Daily"),
    ]
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default=DAILY)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Target: {self.unit}, Amount: {self.amount}"


class Target(models.Model):
    WEEKLY = 'WK'
    DAILY = 'DA'
    UNIT_CHOICES = [
        (WEEKLY, "Weekly"),
        (DAILY, "Daily"),
    ]
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default=DAILY)
    amount = models.IntegerField(default=0)
    total_targets_met = models.IntegerField(default=0)

    def met(self, current):
        met = current == self.amount
        if met:
            self.total_targets_met += 1
            self.save()
        return met


class Streak(models.Model):
    current_streak = models.IntegerField(default=0, null=True, blank=True)
    longest_streak = models.IntegerField(default=0, null=True, blank=True)
    last_reset = models.DateTimeField(auto_now=True)

    def check_streak(self, unit, target, current_applications):
        # get current time
        now = timezone.now()

        # If the target has not been met
        if target > current_applications:
            # If the target is daily
            if unit == Target.DAILY:
                # If the current date is greater
                # than the last reset
                if now.date() > self.last_reset.date():
                    # Reset
                    self.current_streak = 0
                    self.last_reset = now

            # If the target is weekly
            elif unit == Target.WEEKLY:
                # If it is a new week
                if now.isocalendar()[1] != self.last_reset.isocalendar()[1]:
                    # Reset
                    self.current_streak = 0
                    self.last_reset = now
        else:
            # If the target is daily
            if unit == Target.DAILY:
                # If the current date is greater
                # than the last reset
                if now.date() > self.last_reset.date():
                    # Reset
                    self.current_streak += 1
                    self.last_reset = now

            # If the target is weekly
            elif unit == Target.WEEKLY:
                # If it is a new week
                if now.isocalendar()[1] != self.last_reset.isocalendar()[1]:
                    # Reset
                    self.current_streak += 1
                    self.last_reset = now

        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        self.save()


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Non-Binary'),
        ('O', 'Other'),
    )
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile', unique=True)
    email_comms_opt_in = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    target = models.OneToOneField(
        Target, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    streak = models.ForeignKey(
        Streak, on_delete=models.CASCADE, null=True, blank=True, related_name='profile'
    )
    current_applications_made = models.IntegerField(null=True, blank=True)
    last_reset = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def increment_applications(self):
        if self.target.amount > 0:
            self.current_applications_made += 1
            if self.target.met(self.current_applications_made):
                self.streak.current_streak += 1
                self.streak.save()

    def check_streak(self):
        if self.target.amount > 0:
            now = timezone.now()
            self.streak.check_streak(
                self.target.unit, self.current_applications_made)
            # If the target is daily
            if self.target.unit == Target.DAILY:
                # If the current date is greater
                # than the last reset
                if now.date() > self.last_reset.date():
                    # Reset
                    self.current_applications_made = 0
                    self.last_reset = now

            # If the target is weekly
            elif self.target.unit == Target.WEEKLY:
                # If it is a new week
                if now.isocalendar()[1] != self.last_reset.isocalendar()[1]:
                    # Reset
                    self.current_applications_made = 0
                    self.last_reset = now
            self.save()
