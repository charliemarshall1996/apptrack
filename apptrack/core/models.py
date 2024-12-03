from django.db import models
from django.contrib.auth import get_user_model
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from .utils import get_country_choices
User = get_user_model()
# Set up the geolocator with a basic user agent
geolocator = Nominatim(user_agent="your_app_name_or_email")


class Locations(models.Model):
    COUNTRY_CHOICES = get_country_choices()

    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Build the location string for geocoding
        location_query = self.country

        if self.region:
            location_query = f"{self.region}, {self.country}"

        if self.city:
            location_query = f"{self.city}, {self.region}, {self.country}"

        try:
            location = geolocator.geocode(location_query)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
            else:
                self.latitude = None
                self.longitude = None
        except GeocoderTimedOut:
            # Handle timeouts gracefully
            self.latitude = None
            self.longitude = None

        # Call the parent class's save method
        super().save(*args, **kwargs)


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
    alert_type = models.CharField(max_length=20)

    alert_via_email = models.BooleanField(default=False)

    alert_via_push = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False, blank=True)

    persistent = models.BooleanField(default=False)
    persistent_until_read = models.BooleanField(default=False)
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert for {self.user} on {self.interview.job.title} - {self.alert_type}"
