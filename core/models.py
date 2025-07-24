from django.db import models


class Currency(models.Model):
    alpha_3 = models.CharField(max_length=3)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Country(models.Model):
    alpha_2 = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobFunction(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LocationPolicy(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PayRate(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkContract(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
