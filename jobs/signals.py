"""This module contains the signals for the jobs app.

The create_board_on_profile_creation function is called when a new profile is created,
creating a corresponding board for the profile instance. The
create_columns_on_board_creation function is called when a new board is created,
creating default columns for the board.
"""
from django.dispatch import receiver
from django.utils import timezone

from accounts.views import user_login
from core.choices import StatusChoices

from .models import Job, Settings


@receiver(user_login)
def auto_archive(sender, instance, **kwargs):
    profile = instance.profile
    jobs = Job.objects.filter(profile=profile)
    settings, created = Settings.objects.get_or_create(profile=profile)

    if created:
        settings.save()
    for job in jobs:
        if settings.auto_archive and any([job.status == StatusChoices.APPLIED[0],
                                          job.status == StatusChoices.REJECTED[0],
                                          job.status == StatusChoices.CLOSED[0],
                                          job.status == StatusChoices.OPEN[0]]):
            today = timezone.now().date()
            date_diff = today - job.created.date()
            if date_diff.days >= (settings.archive_after_weeks * 7):
                job.archived = True
                job.save()


@receiver(user_login)
def check_jobs(sender, instance, **kwargs):
    profile = instance.profile
    jobs = Job.objects.filter(profile=profile)
    for job in jobs:
        job.save()
