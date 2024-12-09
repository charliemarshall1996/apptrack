
from jobs.choices import (
    PayRateChoices,
    StatusChoices,
    SourceChoices,
)


def test_source_choices():
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

    CHOICES = [
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
        (FREELANCER_NETWORK, "Freelancer Network"),
    ]

    assert SourceChoices.choices() == CHOICES


def test_pay_rate_choices():
    UNKNOWN = "UK"
    HOURLY = "HR"
    DAILY = "DY"
    WEEKLY = "WK"
    MONTHLY = "MO"
    YEARLY = "YR"

    CHOICES = [
        (UNKNOWN, 'Unknown'),
        (HOURLY, 'Hourly'),
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly'),
    ]

    assert PayRateChoices.choices() == CHOICES


def test_status_choices():
    OPEN = "OP"
    APPLIED = "AP"
    REJECTED = "RE"
    SHORTLISTED = "SL"
    INTERVIEW = "IN"
    OFFER = "OF"
    CLOSED = "CL"

    CHOICES = [
        (OPEN, 'Open'),
        (APPLIED, 'Applied'),
        (REJECTED, 'Rejected'),
        (SHORTLISTED, 'Shortlisted'),
        (INTERVIEW, 'Interview'),
        (OFFER, 'Offer'),
        (CLOSED, 'Closed'),
    ]

    assert StatusChoices.choices() == CHOICES


def test_get_status_column():
    OPEN = "OP"
    APPLIED = "AP"
    REJECTED = "RE"
    SHORTLISTED = "SL"
    INTERVIEW = "IN"
    OFFER = "OF"
    CLOSED = "CL"

    status_columns = [
        (OPEN, 1),
        (APPLIED, 2),
        (SHORTLISTED, 3),
        (INTERVIEW, 4),
        (OFFER, 5),
        (REJECTED, 6),
        (CLOSED, 7)
    ]

    for status, column in status_columns:
        assert StatusChoices.get_status_column_position(status) == column


def test_get_column_status():
    OPEN = "OP"
    APPLIED = "AP"
    REJECTED = "RE"
    SHORTLISTED = "SL"
    INTERVIEW = "IN"
    OFFER = "OF"
    CLOSED = "CL"

    status_columns = [
        (OPEN, 1),
        (APPLIED, 2),
        (SHORTLISTED, 3),
        (INTERVIEW, 4),
        (OFFER, 5),
        (REJECTED, 6),
        (CLOSED, 7)
    ]

    for status, column in status_columns:
        assert StatusChoices.get_column_position_status(column) == status


def test_get_column_name():

    status_columns = [
        (1, 'Open'),
        (2, 'Applied'),
        (3, 'Shortlisted'),
        (4, 'Interview'),
        (5, 'Offer'),
        (6, "Rejected"),
        (7, 'Closed'),
    ]

    for column, name in status_columns:
        assert StatusChoices.get_column_position_status_name(column) == name
