from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Company(models.Model):

    UNKNOWN = "unknown"
    START_UP = "startup"
    ESTABLISHED = "established"
    ENTERPRISE = "enterprise"
    SIZE_CHOICES = (
        (START_UP, "startup"),
        (ESTABLISHED, "established"),
        (ENTERPRISE, "enterprise"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    industry = models.CharField(max_length=100)
    is_recruiter = models.BooleanField()

    def __str__(self):
        return self.name

class Jobs(models.Model):

    ARCHIVED = "archived"
    APPLIED = "applied"
    REJECTED = "rejected"
    SHORTLISTED = "shortlisted"
    INTERVIEW = "interview"
    OFFER = "offer"
    OPEN = "open"
    CLOSED = "closed"

    STATUS_CHOICES = (
        (ARCHIVED, "archived"),
        (APPLIED, "applied"),
        (REJECTED, "rejected"),
        (SHORTLISTED, "shortlisted"),
        (INTERVIEW, "interview"),
        (OFFER, "offer"),
        (OPEN, "open"),
        (CLOSED, "closed"),
    )

    WEB = "web"
    HEADHUNTER = "headhunter"
    NEWSPAPER = "newspaper"

    SOURCE_CHOICES = (
        (WEB, "web"),
        (HEADHUNTER, "headhunter"),
        (NEWSPAPER, "newspaper"),
    )

    UNKNOWN = "unknown"
    HYBRID = "hybrid"
    ON_SITE = "onsite"
    REMOTE = "remote"
    FLEXIBLE = "flexible"

    LOCATION_POLICY_CHOICES = (
        (UNKNOWN, "unknown"),
        (HYBRID, "hybrid"),
        (ON_SITE, "onsite"),
        (REMOTE, "remote"),
        (FLEXIBLE, "flexible"),
    )

    FULLTIME = "fulltime"
    PARTTIME = "parttime"
    CONTRACT = "contract"
    SECONDMENT = "secondment"
    WORK_CONTRACT_CHOICES = (
        (UNKNOWN, "unknown"),
        (FULLTIME, "fulltime"),
        (PARTTIME, "parttime"),
        (CONTRACT, "contract"),
        (SECONDMENT, "secondment"),
    )

    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    PAY_RATE_CHOICES = (
        (UNKNOWN, "unknown"),
        (HOURLY, "hourly"),
        (DAILY, "daily"),
        (WEEKLY, "weekly"),
        (MONTHLY, "monthly"),
        (YEARLY, "yearly"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    location_policy = models.CharField(max_length=100, choices=LOCATION_POLICY_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=UNKNOWN)
    work_contract = models.CharField(max_length=100, choices=WORK_CONTRACT_CHOICES, default=UNKNOWN)
    pay_rate = models.CharField(max_length=100, choices=PAY_RATE_CHOICES, default=UNKNOWN)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)