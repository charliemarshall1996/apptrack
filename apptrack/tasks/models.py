
from django.contrib.auth import get_user_model
from django.db import models
from polymorphic.models import PolymorphicModel

User = get_user_model()


class Task(PolymorphicModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)


class InterviewTask(Task):
    interview = models.ForeignKey(
        'interview.Interview', related_name="tasks", on_delete=models.CASCADE)


class JobTask(Task):
    job = models.ForeignKey(
        'jobs.Job', related_name="tasks", on_delete=models.CASCADE)


class TargetTask(Task):
    target = models.ForeignKey(
        'targets.Target', related_name="task", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.target.met:
            self.is_completed = True

        super().save(*args, **kwargs)
