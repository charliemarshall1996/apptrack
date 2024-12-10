
from django.contrib.auth import get_user_model
from django.db import models
from polymorphic.models import PolymorphicModel

User = get_user_model()


class Task(PolymorphicModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0, null=True, blank=True)


class TargetTask(Task):
    target = models.ForeignKey(
        'targets.Target', related_name="task", on_delete=models.CASCADE)

    @property
    def current_val(self):
        return self.target.current

    @property
    def target_val(self):
        return self.target.daily_target

    @property
    def type(self):
        return "target"

    def save(self, *args, **kwargs):
        if self.target.met:
            self.is_completed = True
        self.priority = 1
        super().save(*args, **kwargs)


class InterviewTask(Task):
    interview = models.ForeignKey(
        'interview.Interview', related_name="tasks", on_delete=models.CASCADE)

    @property
    def type(self):
        return "interview"

    def save(self, *args, **kwargs):
        self.priority = 2
        super().save(*args, **kwargs)


class JobTask(Task):
    job = models.ForeignKey(
        'jobs.Job', related_name="tasks", on_delete=models.CASCADE)

    @property
    def type(self):
        return "job"

    def save(self, *args, **kwargs):
        self.priority = 3
        super().save(*args, **kwargs)
