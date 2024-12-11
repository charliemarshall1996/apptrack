from django.db import models


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
