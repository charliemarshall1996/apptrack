
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
import pycountry

from core.models import Locations

# Create your models here.


class Companies(models.Model):

    UNKNOWN = "unknown"
    START_UP = "startup"
    ESTABLISHED = "established"
    ENTERPRISE = "enterprise"
    SIZE_CHOICES = (
        (START_UP, "startup"),
        (ESTABLISHED, "established"),
        (ENTERPRISE, "enterprise"),
    )

    INDUSTRY_CHOICES = [
    ("acct", "Accounting"),
    ("advt", "Advertising"),
    ("aero", "Aerospace"),
    ("agri", "Agriculture"),
    ("apparel", "Apparel & Fashion"),
    ("arch", "Architecture"),
    ("auto", "Automotive"),
    ("aviation", "Aviation"),
    ("bank", "Banking"),
    ("bio", "Biotechnology"),
    ("broadcast", "Broadcast Media"),
    ("build_mat", "Building Materials"),
    ("bus_serv", "Business Services"),
    ("chem", "Chemicals"),
    ("comp_sftw", "Computer Software"),
    ("constr", "Construction"),
    ("cons_goods", "Consumer Goods"),
    ("cons_serv", "Consumer Services"),
    ("defense", "Defense & Space"),
    ("design", "Design"),
    ("edu", "Education"),
    ("elec", "Electronics"),
    ("energy", "Energy"),
    ("eng", "Engineering"),
    ("ent", "Entertainment"),
    ("env_serv", "Environmental Services"),
    ("fin_serv", "Financial Services"),
    ("food_bev", "Food & Beverage"),
    ("govt", "Government"),
    ("health", "Healthcare"),
    ("hosp", "Hospitality"),
    ("hr", "Human Resources"),
    ("it", "Information Technology"),
    ("insurance", "Insurance"),
    ("inv_bank", "Investment Banking"),
    ("legal", "Legal Services"),
    ("logistics", "Logistics & Supply Chain"),
    ("mfg", "Manufacturing"),
    ("mktg", "Marketing"),
    ("media", "Media"),
    ("med_dev", "Medical Devices"),
    ("mining", "Mining"),
    ("non_profit", "Non-profit"),
    ("pharma", "Pharmaceuticals"),
    ("pr", "Public Relations"),
    ("publishing", "Publishing"),
    ("real_est", "Real Estate"),
    ("recruiting", "Recruiting"),
    ("retail", "Retail"),
    ("sports", "Sports"),
    ("tech", "Technology"),
    ("telecom", "Telecommunications"),
    ("transp", "Transportation"),
    ("travel", "Travel & Tourism"),
    ("utilities", "Utilities"),
    ("vc", "Venture Capital"),
    ("wholesale", "Wholesale"),
    ("other", "Other")
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_companies")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updated_companies")
    industry = models.CharField(max_length=10, choices=INDUSTRY_CHOICES, null=True, blank=True)
    is_recruiter = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Jobs(models.Model):

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

    JOB_FUNCTION_CHOICES = [
        ("acct", "Accounting"),
        ("advt", "Advertising"),
        ("aero_eng", "Aerospace Engineering"),
        ("agri", "Agriculture"),
        ("arch", "Architecture"),
        ("auto_eng", "Automotive Engineering"),
        ("aviation", "Aviation"),
        ("banking", "Banking"),
        ("biotech", "Biotechnology"),
        ("broadcast", "Broadcast Media"),
        ("bus_dev", "Business Development"),
        ("bus_ops", "Business Operations"),
        ("chem_eng", "Chemical Engineering"),
        ("comp_eng", "Computer Engineering"),
        ("constr_mgmt", "Construction Management"),
        ("consulting", "Consulting"),
        ("cust_serv", "Customer Service"),
        ("data_sci", "Data Science"),
        ("design", "Design"),
        ("edu", "Education"),
        ("elec_eng", "Electrical Engineering"),
        ("energy", "Energy"),
        ("eng", "Engineering"),
        ("ent", "Entertainment"),
        ("env_sci", "Environmental Science"),
        ("fin", "Finance"),
        ("food_serv", "Food Services"),
        ("govt", "Government"),
        ("health", "Healthcare"),
        ("hr", "Human Resources"),
        ("it", "Information Technology"),
        ("insurance", "Insurance"),
        ("inv_banking", "Investment Banking"),
        ("legal", "Legal"),
        ("logistics", "Logistics"),
        ("mfg", "Manufacturing"),
        ("marketing", "Marketing"),
        ("media", "Media"),
        ("med_dev", "Medical Devices"),
        ("mining", "Mining"),
        ("non_profit", "Non-profit"),
        ("pharma", "Pharmaceuticals"),
        ("pr", "Public Relations"),
        ("project_mgmt", "Project Management"),
        ("real_estate", "Real Estate"),
        ("recruiting", "Recruiting"),
        ("retail", "Retail"),
        ("sales", "Sales"),
        ("sports", "Sports"),
        ("supply_chain", "Supply Chain"),
        ("tech_support", "Technical Support"),
        ("telecom", "Telecommunications"),
        ("transport", "Transportation"),
        ("travel", "Travel & Tourism"),
        ("utilities", "Utilities"),
        ("venture_cap", "Venture Capital"),
        ("wholesale", "Wholesale"),
        ("other", "Other")
    ]

    PAY_CURRENCY_CHOICES = [(currency.alpha_3, currency.alpha_3) for currency in pycountry.currencies]

    id = models.BigAutoField(primary_key=True)

    url = models.URLField(blank=True, null=True, unique=True)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES)
    
    job_title = models.CharField(max_length=100)
    job_function = models.CharField(max_length=100, choices=JOB_FUNCTION_CHOICES, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    location_policy = models.CharField(max_length=100, choices=LOCATION_POLICY_CHOICES, null=True, blank=True)
    work_contract = models.CharField(max_length=100, choices=WORK_CONTRACT_CHOICES, null=True, blank=True)

    min_pay = models.IntegerField(null=True, blank=True)
    max_pay = models.IntegerField(null=True, blank=True)
    pay_rate = models.CharField(max_length=100, choices=PAY_RATE_CHOICES, null=True, blank=True)
    currency = models.CharField(max_length=100, null=True, blank=True)

    # company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True)
    # location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updated_by", null=True, blank=True)

    users = models.ManyToManyField(User, related_name="users", blank=True)

class UserJobsDetails(models.Model):

    ARCHIVED = "arc"
    APPLIED = "app"
    REJECTED = "rej"
    SHORTLISTED = "sli"
    INTERVIEW = "int"
    OFFER = "off"
    OPEN = "ope"
    CLOSED = "clo"

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


    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, null=True, blank=True)