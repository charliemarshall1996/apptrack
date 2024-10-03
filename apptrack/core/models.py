from django.db import models
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from .utils import get_country_choices

# Set up the geolocator with a basic user agent
geolocator = Nominatim(user_agent="your_app_name_or_email")

class Locations(models.Model):
    COUNTRY_CHOICES = get_country_choices()

    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

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

    
