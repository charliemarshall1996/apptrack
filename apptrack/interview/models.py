from django.db import models
from django.conf import settings
from core.models import Task
# Create your models here.


class InterviewTask(Task):
    interview = models.ForeignKey(
        'Interview', on_delete=models.CASCADE, related_name='tasks')


class Interview(models.Model):
    interview_round = models.IntegerField(default=1)
    job = models.ForeignKey(
        'jobs.Job', on_delete=models.CASCADE, related_name='interviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    post_code = models.CharField(max_length=10, blank=True, null=True)
    building = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=20, blank=True, null=True)
    town = models.CharField(max_length=20, blank=True, null=True)
    region = models.CharField(max_length=20, blank=True, null=True)
    meeting_url = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.job.job_title} at {self.job.company}"

    def create_default_tasks(self):
        default_tasks = [
            "Prepare for interview",
            "Review job description",
            "Research the company",
            "Prepare questions for the interviewer",
            "Dress appropriately",
            "Plan your route to the interview",
        ]
        for task in default_tasks:
            InterviewTask.objects.create(interview=self, name=task)

    def save(self, *args, **kwargs):
        if not self.pk:  # This ensures tasks are added only once when the interview is created
            super().save(*args, **kwargs)
            self.create_default_tasks()
        else:
            super().save(*args, **kwargs)


class Interviewer(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    title = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.job.title} at {self.job.company}"
