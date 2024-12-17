
import logging

from django.db import models
from polymorphic.models import PolymorphicModel

from accounts.models import Profile
from jobs.models import Job, Interview
from target.models import Target
# Create your models here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create your models here.


class Task(PolymorphicModel):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0, null=True, blank=True)


class TargetTask(Task):
    target = models.ForeignKey(
        Target, related_name="task", on_delete=models.CASCADE)

    @property
    def current_val(self):
        return self.target.current

    @property
    def target_val(self):
        return self.target.amount

    @property
    def type(self):
        return "target"

    def save(self, *args, **kwargs):
        if self.target.met:
            logger.info("Target met %s %s", self.target.amount,
                        self.target.current)
            self.is_completed = True
        self.priority = 1
        super().save(*args, **kwargs)


class InterviewTask(Task):
    interview = models.ForeignKey(
        Interview, related_name="tasks", on_delete=models.CASCADE)

    @property
    def type(self):
        return "interview"

    def save(self, *args, **kwargs):
        self.priority = 2
        super().save(*args, **kwargs)


class JobTask(Task):
    job = models.ForeignKey(
        Job, related_name="tasks", on_delete=models.CASCADE)

    @property
    def type(self):
        return "job"

    def save(self, *args, **kwargs):
        self.priority = 3
        super().save(*args, **kwargs)
