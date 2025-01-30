from django.db import models

from accounts.models import Profile
# Create your models here.


class Company(models.Model):
    profile = models.ForeignKey(
        Profile, related_name="company", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_recruiter = models.BooleanField(default=False)
    website = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    employees = models.IntegerField(null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    ignore = models.BooleanField(default=False)

    def __str__(self):
        return self.name
