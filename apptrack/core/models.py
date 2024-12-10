from django.db import models
from django.contrib.auth import get_user_model

from .choices import ReminderUnitChoices

User = get_user_model()


class Reminder(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    offset = models.IntegerField(default=1)
    unit = models.CharField(
        max_length=1, choices=ReminderUnitChoices.choices())

    emailed = models.BooleanField(default=False, blank=True)
    read = models.BooleanField(default=False)


class Currency(models.Model):
    iso3 = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Country(models.Model):
    iso2 = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
