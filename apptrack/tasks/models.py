"""Tasks models."""

import logging

from django.db import models
from polymorphic.models import PolymorphicModel

from accounts.models import Profile
# Create your models here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create your models here.


class Task(PolymorphicModel):
    """Tasks model."""

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0, null=True, blank=True)


class InterviewTask(Task):
    """Interview task model."""

    interview = models.ForeignKey(
        "jobs.Interview", related_name="tasks", on_delete=models.CASCADE
    )

    @property
    def type(self):
        """Get task type."""
        return "interview"

    def save(self, *args, **kwargs):
        """Save method for InterviewTask.

        Sets the priority to 2 before saving the instance.
        """
        self.priority = 2
        super().save(*args, **kwargs)


class JobTask(Task):
    """Job task model."""

    job = models.ForeignKey(
        "jobs.Job", related_name="tasks", on_delete=models.CASCADE)

    @property
    def type(self):
        """Get task type."""
        return "job"

    def save(self, *args, **kwargs):
        """Save method for JobTask.

        Sets the priority to 3 before saving the instance.
        """
        self.priority = 3
        super().save(*args, **kwargs)
