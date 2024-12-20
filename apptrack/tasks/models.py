"""Tasks models."""

import logging

from django.db import models
from polymorphic.models import PolymorphicModel

from accounts.models import Profile
from target.models import Target
# Create your models here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create your models here.


class Task(PolymorphicModel):
    """Tasks model."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0, null=True, blank=True)


class TargetTask(Task):
    """Target task model."""

    target = models.ForeignKey(Target, related_name="task", on_delete=models.CASCADE)

    @property
    def current_val(self):
        """Get current value."""
        return self.target.current

    @property
    def target_val(self):
        """Get target value."""
        return self.target.amount

    @property
    def type(self):
        """Get task type."""
        return "target"

    def save(self, *args, **kwargs):
        """Save method for TargetTask.

        Sets the priority to 1 and checks if the target is met.
        If the target is met, logs the target details and marks the task as completed.
        Calls the superclass's save method to persist the changes.
        """
        if self.target.met:
            logger.info("Target met %s %s", self.target.amount, self.target.current)
            self.is_completed = True
        self.priority = 1
        super().save(*args, **kwargs)


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

    job = models.ForeignKey("jobs.Job", related_name="tasks", on_delete=models.CASCADE)

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
