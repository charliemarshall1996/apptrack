
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from accounts.models import Profile
from company.models import Company
from core.models import (
    Country,
    Currency,
    JobFunction,
    LocationPolicy,
    WorkContract,
    PayRate,
)

from core.choices import StatusChoices, SourceChoices

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create your models here.


class Job(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    url = models.URLField(blank=True, null=True)
    source = models.CharField(
        max_length=2, choices=SourceChoices.choices(), null=True, blank=True
    )

    job_title = models.CharField(max_length=100, blank=True, null=True)
    job_function = models.ForeignKey(
        JobFunction, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    is_recruiter = models.BooleanField(default=False, null=True, blank=True)

    location_policy = models.ForeignKey(
        LocationPolicy, on_delete=models.SET_NULL, null=True, blank=True
    )
    work_contract = models.ForeignKey(
        WorkContract, on_delete=models.SET_NULL, null=True, blank=True
    )

    min_pay = models.IntegerField(null=True, blank=True)
    max_pay = models.IntegerField(null=True, blank=True)
    pay_rate = models.ForeignKey(
        PayRate, on_delete=models.SET_NULL, null=True, blank=True
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, blank=True
    )

    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )

    note = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=2, choices=StatusChoices.choices(), default=StatusChoices.default()
    )

    applied = models.BooleanField(null=True, blank=True)
    date_applied = models.DateField(null=True, blank=True)

    interviewed = models.BooleanField(null=True, blank=True)
    date_interviewed_set = models.DateField(null=True, blank=True)

    offered = models.BooleanField(null=True, blank=True)
    date_offered_set = models.DateField(null=True, blank=True)

    archived = models.BooleanField(null=True, blank=True, default=False)
    has_been_archived = models.BooleanField(
        null=True, blank=True, default=False)

    def __str__(self):
        return f"{self.company} - {self.job_title}"

    def _update_if_changed(self):
        if self.pk:
            logger.debug("PK exists")
            original = Job.objects.filter(pk=self.pk).first()
            if not original:
                logger.debug("Original does not exist")
                self.updated = timezone.now()
            else:
                logger.debug("Original exists")
                if original.status != self.status or original.note != self.note:
                    logger.debug("Status or note has changed")
                    logger.info("Updating job...")
                    self.updated = timezone.now()

    def _set_applied(self):
        logger.info("Setting applied...")

        try:
            if self.status in StatusChoices.get_applied_statuses():
                logger.info("Job is applied")

                if not self.applied:
                    self.applied = True

                if not self.date_applied:
                    self.date_applied = timezone.now()

            else:
                if self.status == StatusChoices.OPEN[0]:
                    logger.info("Job is not applied")

                    if self.applied:
                        self.applied = False

                    if self.date_applied:
                        self.date_applied = None

        except Job.DoesNotExist:
            pass

    def _set_interviewed(self):
        logger.info("Setting interviewed...")
        if self.status in [StatusChoices.INTERVIEW, StatusChoices.OFFER]:
            self.interviewed = True
            if not self.date_interviewed_set:
                self.date_interviewed_set = timezone.now()

    def save(self, *args, **kwargs):
        self._update_if_changed()
        self._set_applied()
        self._set_interviewed()
        super().save(*args, **kwargs)


class Settings(models.Model):
    """This model represents the job settings for a user."""

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="job_settings"
    )

    auto_archive = models.BooleanField(null=True, blank=True, default=True)
    archive_after_weeks = models.IntegerField(null=True, blank=True, default=2)
