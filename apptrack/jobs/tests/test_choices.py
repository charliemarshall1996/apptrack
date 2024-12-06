
from jobs.choices import (
    CurrencyChoices,
    CountryChoices,
    JobFunctionChoices,
    LocationPolicyChoices,
    WorkContractChoices,
    PayRateChoices,
    StatusChoices,
    SourceChoices,
)


def test_currency_choices():
    print(CurrencyChoices.choices())


def test_country_choices():
    print(CountryChoices.choices())


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


def test_location_policy_choices():
    UNKNOWN = "UK"
    HYBRID = "HY"
    ON_SITE = "ON"
    REMOTE = "RE"
    FLEXIBLE = "FL"

    CHOICES = [
        (UNKNOWN, 'Unknown'),
        (HYBRID, 'Hybrid'),
        (ON_SITE, 'On-Site'),
        (REMOTE, 'Remote'),
        (FLEXIBLE, 'Flexible'),
    ]

    assert LocationPolicyChoices.choices() == CHOICES


def test_work_contract_choices():
    UNKNOWN = "UK"
    FULLTIME = "FT"
    PARTTIME = "PT"
    CONTRACT = "CO"
    SECONDMENT = "SE"

    CHOICES = [
        (UNKNOWN, 'Unknown'),
        (FULLTIME, 'Fulltime'),
        (PARTTIME, 'Parttime'),
        (CONTRACT, 'Contract'),
        (SECONDMENT, 'Secondment'),
    ]

    assert WorkContractChoices.choices() == CHOICES


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


def test_job_function_choices():
    ACCOUNTING = "AC"
    ADVERTISING = "AD"
    AEROSPACE_ENGINEERING = "AE"
    AGRICULTURE = "AG"
    ARCHITECTURE = "AR"
    AUTOMOTIVE_ENGINEERING = "AU"
    AVIATION = "AV"
    BANKING = "BA"
    BIOTECHNOLOGY = "BI"
    BROADCAST_MEDIA = "BM"
    BUSINESS_DEVELOPMENT = "BD"
    BUSINESS_OPERATIONS = "BO"
    CHEMICAL_ENGINEERING = "CE"
    COMPUTER_ENGINEERING = "CO"
    CONSTRUCTION_MANAGEMENT = "CM"
    CONSULTING = "CN"
    CUSTOMER_SERVICE = "CS"
    DATA_SCIENCE = "DS"
    DESIGN = "DE"
    EDUCATION = "ED"
    ELECTRICAL_ENGINEERING = "EE"
    ENERGY = "EN"
    ENGINEERING = "EG"
    ENTERTAINMENT = "ET"
    ENVIRONMENTAL_SCIENCE = "ES"
    FINANCE = "FI"
    FOOD_SERVICES = "FS"
    GOVERNMENT = "GO"
    HEALTHCARE = "HE"
    HUMAN_RESOURCES = "HR"
    INFORMATION_TECHNOLOGY = "IT"
    INSURANCE = "IN"
    INVESTMENT_BANKING = "IB"
    LEGAL = "LE"
    LOGISTICS = "LO"
    MANUFACTURING = "MF"
    MARKETING = "MK"
    MEDIA = "MD"
    MEDICAL_DEVICES = "ME"
    MINING = "MI"
    NON_PROFIT = "NP"
    PHARMACEUTICALS = "PH"
    PUBLIC_RELATIONS = "PR"
    PROJECT_MANAGEMENT = "PM"
    REAL_ESTATE = "RE"
    RECRUITING = "RC"
    RETAIL = "RT"
    SALES = "SA"
    SPORTS = "SP"
    SUPPLY_CHAIN = "SC"
    TECHNICAL_SUPPORT = "TS"
    TELECOMMUNICATIONS = "TC"
    TRANSPORTATION = "TR"
    TRAVEL_TOURISM = "TT"
    UTILITIES = "UT"
    VENTURE_CAPITAL = "VC"
    WHOLESALE = "WH"
    OTHER = "OT"

    CHOICES = [
        (ACCOUNTING, 'Accounting'),
        (ADVERTISING, 'Advertising'),
        (AEROSPACE_ENGINEERING, 'Aerospace Engineering'),
        (AGRICULTURE, 'Agriculture'),
        (ARCHITECTURE, 'Architecture'),
        (AUTOMOTIVE_ENGINEERING, 'Automotive Engineering'),
        (AVIATION, 'Aviation'),
        (BANKING, 'Banking'),
        (BIOTECHNOLOGY, 'Biotechnology'),
        (BROADCAST_MEDIA, 'Broadcast Media'),
        (BUSINESS_DEVELOPMENT, 'Business Development'),
        (BUSINESS_OPERATIONS, 'Business Operations'),
        (CHEMICAL_ENGINEERING, 'Chemical Engineering'),
        (COMPUTER_ENGINEERING, 'Computer Engineering'),
        (CONSTRUCTION_MANAGEMENT, 'Construction Management'),
        (CONSULTING, 'Consulting'),
        (CUSTOMER_SERVICE, 'Customer Service'),
        (DATA_SCIENCE, 'Data Science'),
        (DESIGN, 'Design'),
        (EDUCATION, 'Education'),
        (ELECTRICAL_ENGINEERING, 'Electrical Engineering'),
        (ENERGY, 'Energy'),
        (ENGINEERING, 'Engineering'),
        (ENTERTAINMENT, 'Entertainment'),
        (ENVIRONMENTAL_SCIENCE, 'Environmental Science'),
        (FINANCE, 'Finance'),
        (FOOD_SERVICES, 'Food Services'),
        (GOVERNMENT, 'Government'),
        (HEALTHCARE, 'Healthcare'),
        (HUMAN_RESOURCES, 'Human Resources'),
        (INFORMATION_TECHNOLOGY, 'Information Technology'),
        (INSURANCE, 'Insurance'),
        (INVESTMENT_BANKING, 'Investment Banking'),
        (LEGAL, 'Legal'),
        (LOGISTICS, 'Logistics'),
        (MANUFACTURING, 'Manufacturing'),
        (MARKETING, 'Marketing'),
        (MEDIA, 'Media'),
        (MEDICAL_DEVICES, 'Medical Devices'),
        (MINING, 'Mining'),
        (NON_PROFIT, 'Non-profit'),
        (PHARMACEUTICALS, 'Pharmaceuticals'),
        (PUBLIC_RELATIONS, 'Public Relations'),
        (PROJECT_MANAGEMENT, 'Project Management'),
        (REAL_ESTATE, 'Real Estate'),
        (RECRUITING, 'Recruiting'),
        (RETAIL, 'Retail'),
        (SALES, 'Sales'),
        (SPORTS, 'Sports'),
        (SUPPLY_CHAIN, 'Supply Chain'),
        (TECHNICAL_SUPPORT, 'Technical Support'),
        (TELECOMMUNICATIONS, 'Telecommunications'),
        (TRANSPORTATION, 'Transportation'),
        (TRAVEL_TOURISM, 'Travel & Tourism'),
        (UTILITIES, 'Utilities'),
        (VENTURE_CAPITAL, 'Venture Capital'),
        (WHOLESALE, 'Wholesale'),
        (OTHER, 'Other'),
    ]

    assert JobFunctionChoices.choices() == CHOICES


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
