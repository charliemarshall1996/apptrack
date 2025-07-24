from django.db import models

from accounts.models import Profile
from core.models import Country
from jobs.models import Job
# Create your models here.


class Interview(models.Model):
    interview_round = models.IntegerField(default=1)
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name="interviews")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    round = models.IntegerField(default=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    post_code = models.CharField(max_length=10, blank=True, null=True)
    building = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    region = models.CharField(max_length=20, blank=True, null=True)
    meeting_url = models.URLField(blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.job.job_title} at {self.job.company}"
