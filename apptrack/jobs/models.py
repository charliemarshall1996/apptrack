
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core.utils import get_currency_choices, get_country_choices


User = get_user_model()


# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=255, null=True,
                            blank=True, default="My Job Board")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='board')

    def save(self, *args, **kwargs):
        if not self.name or self.name == 'None':
            self.name = "My Job Board"

        super().save(*args, **kwargs)

        default_columns = [
            ('Open', 1),
            ('Applied', 2),
            ('Shortlisted', 3),
            ('Interview', 4),
            ('Offer', 5),
            ('Rejected', 6),
            ('Closed', 7),
        ]

        for name, position in default_columns:
            if not Column.objects.filter(name=name, board=self).exists():
                column = Column(name=name, position=position, board=self)
                column.save()
                print(f"Column added: {column.name}")

        if not self.columns.exists():
            columns_to_add = Column.objects.all()
            self.columns.add(*columns_to_add)
            print(f"Columns added: {columns_to_add}")


class Column(models.Model):
    board = models.ForeignKey(
        'Board', on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255)
    position = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']
        unique_together = ('board', 'name', 'position')


class Job(models.Model):

    WEB = "WW"
    HEADHUNTER = "HH"
    NEWSPAPER = "NP"
    COMPANY_WEBSITE = "CW"
    REFERRAL = "RF"
    JOB_BOARD = "JB"
    RECRUITMENT_AGENCY = "RA"
    SOCIAL_MEDIA = "SM"
    CAREER_FAIR = "CF"
    INTERNAL_POSTING = "IP"
    FREELANCE_PLATFORM = "FP"
    UNIVERSITY_CAREER_SERVICES = "UC"
    NETWORKING_EVENT = "NE"
    PROFESSIONAL_ASSOCIATION = "PA"
    GOVERNMENT_PORTAL = "GP"
    COLD_OUTREACH = "CO"
    JOB_NEWSLETTER = "JN"
    FREELANCER_NETWORK = "FN"

    SOURCE_CHOICES = (
        (WEB, "Web"),
        (HEADHUNTER, "Headhunter"),
        (NEWSPAPER, "Newspaper"),
        (COMPANY_WEBSITE, "Company Website"),
        (REFERRAL, "Referral"),
        (JOB_BOARD, "Job Board"),
        (RECRUITMENT_AGENCY, "Recruitment Agency"),
        (SOCIAL_MEDIA, "Social Media"),
        (CAREER_FAIR, "Career Fair"),
        (INTERNAL_POSTING, "Internal Posting"),
        (FREELANCE_PLATFORM, "Freelance Platform"),
        (UNIVERSITY_CAREER_SERVICES, "University Career Services"),
        (NETWORKING_EVENT, "Networking Event"),
        (PROFESSIONAL_ASSOCIATION, "Professional Association"),
        (GOVERNMENT_PORTAL, "Government Job Portal"),
        (COLD_OUTREACH, "Cold Outreach"),
        (JOB_NEWSLETTER, "Job Newsletter"),
        (FREELANCER_NETWORK, "Freelancer Network")
    )
    UNKNOWN = "UK"
    HYBRID = "HY"
    ON_SITE = "ON"
    REMOTE = "RE"
    FLEXIBLE = "FL"

    LOCATION_POLICY_CHOICES = (
        (UNKNOWN, "Unknown"),
        (HYBRID, "Hybrid"),
        (ON_SITE, "On-Site"),
        (REMOTE, "Remote"),
        (FLEXIBLE, "Flexible"),
    )

    FULLTIME = "FT"
    PARTTIME = "PT"
    CONTRACT = "CO"
    SECONDMENT = "SE"
    WORK_CONTRACT_CHOICES = (
        (UNKNOWN, "Unknown"),
        (FULLTIME, "Fulltime"),
        (PARTTIME, "Parttime"),
        (CONTRACT, "Contract"),
        (SECONDMENT, "Secondment"),
    )

    HOURLY = "HR"
    DAILY = "DY"
    WEEKLY = "WK"
    MONTHLY = "MO"
    YEARLY = "YR"
    PAY_RATE_CHOICES = (
        (UNKNOWN, "Unknown"),
        (HOURLY, "Hourly"),
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (MONTHLY, "Monthly"),
        (YEARLY, "Yearly"),
    )

    JOB_FUNCTION_CHOICES = [
        ("AC", "Accounting"),
        ("AD", "Advertising"),
        ("AE", "Aerospace Engineering"),
        ("AG", "Agriculture"),
        ("AR", "Architecture"),
        ("AU", "Automotive Engineering"),
        ("AV", "Aviation"),
        ("BA", "Banking"),
        ("BI", "Biotechnology"),
        ("BM", "Broadcast Media"),
        ("BD", "Business Development"),
        ("BO", "Business Operations"),
        ("CE", "Chemical Engineering"),
        ("CO", "Computer Engineering"),
        ("CM", "Construction Management"),
        ("CN", "Consulting"),
        ("CS", "Customer Service"),
        ("DS", "Data Science"),
        ("DE", "Design"),
        ("ED", "Education"),
        ("EE", "Electrical Engineering"),
        ("EN", "Energy"),
        ("EG", "Engineering"),
        ("ET", "Entertainment"),
        ("ES", "Environmental Science"),
        ("FI", "Finance"),
        ("FS", "Food Services"),
        ("GO", "Government"),
        ("HE", "Healthcare"),
        ("HR", "Human Resources"),
        ("IT", "Information Technology"),
        ("IN", "Insurance"),
        ("IB", "Investment Banking"),
        ("LE", "Legal"),
        ("LO", "Logistics"),
        ("MF", "Manufacturing"),
        ("MK", "Marketing"),
        ("MD", "Media"),
        ("ME", "Medical Devices"),
        ("MI", "Mining"),
        ("NP", "Non-profit"),
        ("PH", "Pharmaceuticals"),
        ("PR", "Public Relations"),
        ("PM", "Project Management"),
        ("RE", "Real Estate"),
        ("RC", "Recruiting"),
        ("RT", "Retail"),
        ("SA", "Sales"),
        ("SP", "Sports"),
        ("SC", "Supply Chain"),
        ("TS", "Technical Support"),
        ("TC", "Telecommunications"),
        ("TR", "Transportation"),
        ("TT", "Travel & Tourism"),
        ("UT", "Utilities"),
        ("VC", "Venture Capital"),
        ("WH", "Wholesale"),
        ("OT", "Other")
    ]

    APPLIED = "AP"
    REJECTED = "RE"
    SHORTLISTED = "SL"
    INTERVIEW = "IN"
    OFFER = "OF"
    OPEN = "OP"
    CLOSED = "CL"

    STATUS_CHOICES = (
        (APPLIED, "applied"),
        (REJECTED, "rejected"),
        (SHORTLISTED, "shortlisted"),
        (INTERVIEW, "interview"),
        (OFFER, "offer"),
        (OPEN, "open"),
        (CLOSED, "closed"),
    )

    STATUS_POSITIONS = {
        OPEN: 1,
        APPLIED: 2,
        SHORTLISTED: 3,
        INTERVIEW: 4,
        OFFER: 5,
        REJECTED: 6,
        CLOSED: 7
    }

    POSITION_STATUSES = {
        1: OPEN,
        2: APPLIED,
        3: SHORTLISTED,
        4: INTERVIEW,
        5: OFFER,
        6: REJECTED,
        7: CLOSED
    }

    APPLIED_STATUSES = [APPLIED, SHORTLISTED, INTERVIEW, OFFER, REJECTED]

    PAY_CURRENCY_CHOICES = get_currency_choices()
    COUNTRY_CHOICES = get_country_choices()

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    url = models.URLField(blank=True, null=True)
    source = models.CharField(
        max_length=2, choices=SOURCE_CHOICES, null=True, blank=True)

    job_title = models.CharField(max_length=100, blank=True, null=True)
    job_function = models.CharField(
        max_length=2, choices=JOB_FUNCTION_CHOICES, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    company = models.CharField(max_length=100, null=True, blank=True)
    is_recruiter = models.BooleanField(default=False, null=True, blank=True)

    location_policy = models.CharField(
        max_length=100, choices=LOCATION_POLICY_CHOICES, null=True, blank=True)
    work_contract = models.CharField(
        max_length=100, choices=WORK_CONTRACT_CHOICES, null=True, blank=True)

    min_pay = models.IntegerField(null=True, blank=True)
    max_pay = models.IntegerField(null=True, blank=True)
    pay_rate = models.CharField(
        max_length=2, choices=PAY_RATE_CHOICES, null=True, blank=True)
    currency = models.CharField(
        max_length=3, null=True, blank=True, choices=PAY_CURRENCY_CHOICES)

    town = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(
        max_length=2, choices=COUNTRY_CHOICES, null=True, blank=True)

    note = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=OPEN)
    column = models.ForeignKey(
        Column, related_name="column", on_delete=models.CASCADE, null=True, blank=True)
    board = models.ForeignKey(
        Board, related_name="jobs", on_delete=models.CASCADE, null=True, blank=True)
    applied = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.job_title}"

    def save(self, *args, **kwargs):

        # If the board is not set,
        # set it to the column's board
        if not self.board and self.column:
            self.board = self.column.board

        try:
            if not self.column.board:
                self.column.board = self.board
        except AttributeError:
            pass

        # Check if the column
        # is not already set
        if not self.column and self.board:
            try:
                position = self.STATUS_POSITIONS[self.status]
                name = dict(self.STATUS_CHOICES)[
                    self.POSITION_STATUSES[position]].title()

                # Retrieve the correct column
                # based on the position and board
                col, created = Column.objects.get_or_create(
                    name=name,
                    position=position,
                    board=self.board
                )

                if created:
                    col.save()
                self.column = col
            except ObjectDoesNotExist:
                raise ValueError(
                    f"Column with position {self.STATUS_POSITIONS[self.status]} for board {self.board} does not exist.")

        elif self.column:
            self.column.board = self.board
            # Ensure status is updated based on column position
            self.status = self.POSITION_STATUSES[self.column.position]
            self.column.save()

        # Check if the job is in an applied status
        self.applied = self.status in self.APPLIED_STATUSES

        # Call the parent's save method to persist the object
        super().save(*args, **kwargs)
