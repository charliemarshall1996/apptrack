from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Alert(models.Model):
    DAYS = "d"
    HOURS = "h"
    MINUTES = "m"

    ALERT_BEFORE_UNITS = [
        (DAYS, "Days"),
        (HOURS, "Hours"),
        (MINUTES, "Minutes"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    alert_before = models.IntegerField(default=1)
    alert_before_unit = models.CharField(
        max_length=1, choices=ALERT_BEFORE_UNITS)

    emailed = models.BooleanField(default=False, blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert for {self.user} on {self.interview.job.title} - {self.alert_type}"
