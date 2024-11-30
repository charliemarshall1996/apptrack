
from core.utils import get_country_choices, get_currency_choices


class ChoiceBase:
    @classmethod
    def choices(cls):
        print(f"CHOICES KEYS: {cls.__dict__.keys()}")
        print(f"CHOICES VALUES: {cls.__dict__.values()}")
        # Filter attributes that are tuples of length 2 (value and label)
        return [
            (value[0], value[1])
            for value in cls.__dict__.values()
            if isinstance(value, tuple) and len(value) == 2
        ]


class CurrencyChoices(ChoiceBase):
    @classmethod
    def choices(cls):
        return get_currency_choices()


class CountryChoices(ChoiceBase):
    @classmethod
    def choices(cls):
        return get_country_choices()


class SourceChoices(ChoiceBase):
    WEB = "WW", "Web"
    HEADHUNTER = "HH", "Headhunter"
    NEWSPAPER = "NP", "Newspaper"
    COMPANY_WEBSITE = "CW", "Company Website"
    REFERRAL = "RF", "Referral"
    JOB_BOARD = "JB", "Job Board"
    RECRUITMENT_AGENCY = "RA", "Recruitment Agency"
    SOCIAL_MEDIA = "SM", "Social Media"
    CAREER_FAIR = "CF", "Career Fair"
    INTERNAL_POSTING = "IP", "Internal Posting"
    FREELANCE_PLATFORM = "FP", "Freelance Platform"
    UNIVERSITY_CAREER_SERVICES = "UC", "University Career Services"
    NETWORKING_EVENT = "NE", "Networking Event"
    PROFESSIONAL_ASSOCIATION = "PA", "Professional Association"
    GOVERNMENT_PORTAL = "GP", "Government Job Portal"
    COLD_OUTREACH = "CO", "Cold Outreach"
    JOB_NEWSLETTER = "JN", "Job Newsletter"
    FREELANCER_NETWORK = "FN", "Freelancer Network"


class LocationPolicyChoices(ChoiceBase):
    UNKNOWN = "UK", "Unknown"
    HYBRID = "HY", "Hybrid"
    ON_SITE = "ON", "On-Site"
    REMOTE = "RE", "Remote"
    FLEXIBLE = "FL", "Flexible"


class WorkContractChoices(ChoiceBase):
    UNKNOWN = "UK", "Unknown"
    FULLTIME = "FT", "Fulltime"
    PARTTIME = "PT", "Parttime"
    CONTRACT = "CO", "Contract"
    SECONDMENT = "SE", "Secondment"


class StatusChoices(ChoiceBase):
    OPEN = "OP", "Open"
    APPLIED = "AP", "Applied"
    REJECTED = "RE", "Rejected"
    SHORTLISTED = "SL", "Shortlisted"
    INTERVIEW = "IN", "Interview"
    OFFER = "OF", "Offer"
    CLOSED = "CL", "Closed"

    STATUS_COLUMNS = {
        OPEN[0]: 1,
        APPLIED[0]: 2,
        SHORTLISTED[0]: 3,
        INTERVIEW[0]: 4,
        OFFER[0]: 5,
        REJECTED[0]: 6,
        CLOSED[0]: 7
    }

    COLUMN_STATUSES = {
        1: OPEN,
        2: APPLIED,
        3: SHORTLISTED,
        4: INTERVIEW,
        5: OFFER,
        6: REJECTED,
        7: CLOSED
    }

    APPLIED_STATUSES = [APPLIED, SHORTLISTED, INTERVIEW, OFFER, REJECTED]

    @classmethod
    def get_status_column(cls, status):
        return cls.STATUS_COLUMNS[status]

    @classmethod
    def get_column_status(cls, position: int):
        return cls.COLUMN_STATUSES[position][0]

    @classmethod
    def get_column_name(cls, position: int):
        return cls.COLUMN_STATUSES[position][1]

    @classmethod
    def get_applied_statuses(cls):
        return cls.APPLIED_STATUSES

    @classmethod
    def default(cls):
        return cls.OPEN[0]


class JobFunctionChoices(ChoiceBase):
    ACCOUNTING = "AC", "Accounting"
    ADVERTISING = "AD", "Advertising"
    AEROSPACE_ENGINEERING = "AE", "Aerospace Engineering"
    AGRICULTURE = "AG", "Agriculture"
    ARCHITECTURE = "AR", "Architecture"
    AUTOMOTIVE_ENGINEERING = "AU", "Automotive Engineering"
    AVIATION = "AV", "Aviation"
    BANKING = "BA", "Banking"
    BIOTECHNOLOGY = "BI", "Biotechnology"
    BROADCAST_MEDIA = "BM", "Broadcast Media"
    BUSINESS_DEVELOPMENT = "BD", "Business Development"
    BUSINESS_OPERATIONS = "BO", "Business Operations"
    CHEMICAL_ENGINEERING = "CE", "Chemical Engineering"
    COMPUTER_ENGINEERING = "CO", "Computer Engineering"
    CONSTRUCTION_MANAGEMENT = "CM", "Construction Management"
    CONSULTING = "CN", "Consulting"
    CUSTOMER_SERVICE = "CS", "Customer Service"
    DATA_SCIENCE = "DS", "Data Science"
    DESIGN = "DE", "Design"
    EDUCATION = "ED", "Education"
    ELECTRICAL_ENGINEERING = "EE", "Electrical Engineering"
    ENERGY = "EN", "Energy"
    ENGINEERING = "EG", "Engineering"
    ENTERTAINMENT = "ET", "Entertainment"
    ENVIRONMENTAL_SCIENCE = "ES", "Environmental Science"
    FINANCE = "FI", "Finance"
    FOOD_SERVICES = "FS", "Food Services"
    GOVERNMENT = "GO", "Government"
    HEALTHCARE = "HE", "Healthcare"
    HUMAN_RESOURCES = "HR", "Human Resources"
    INFORMATION_TECHNOLOGY = "IT", "Information Technology"
    INSURANCE = "IN", "Insurance"
    INVESTMENT_BANKING = "IB", "Investment Banking"
    LEGAL = "LE", "Legal"
    LOGISTICS = "LO", "Logistics"
    MANUFACTURING = "MF", "Manufacturing"
    MARKETING = "MK", "Marketing"
    MEDIA = "MD", "Media"
    MEDICAL_DEVICES = "ME", "Medical Devices"
    MINING = "MI", "Mining"
    NON_PROFIT = "NP", "Non-profit"
    PHARMACEUTICALS = "PH", "Pharmaceuticals"
    PUBLIC_RELATIONS = "PR", "Public Relations"
    PROJECT_MANAGEMENT = "PM", "Project Management"
    REAL_ESTATE = "RE", "Real Estate"
    RECRUITING = "RC", "Recruiting"
    RETAIL = "RT", "Retail"
    SALES = "SA", "Sales"
    SPORTS = "SP", "Sports"
    SUPPLY_CHAIN = "SC", "Supply Chain"
    TECHNICAL_SUPPORT = "TS", "Technical Support"
    TELECOMMUNICATIONS = "TC", "Telecommunications"
    TRANSPORTATION = "TR", "Transportation"
    TRAVEL_TOURISM = "TT", "Travel & Tourism"
    UTILITIES = "UT", "Utilities"
    VENTURE_CAPITAL = "VC", "Venture Capital"
    WHOLESALE = "WH", "Wholesale"
    OTHER = "OT", "Other"


class PayRateChoices(ChoiceBase):
    UNKNOWN = "UK", "Unknown"
    HOURLY = "HR", "Hourly"
    DAILY = "DY", "Daily"
    WEEKLY = "WK", "Weekly"
    MONTHLY = "MO", "Monthly"
    YEARLY = "YR", "Yearly"


class WorkContractChoices(ChoiceBase):
    UNKNOWN = "UK", "Unknown"
    FULLTIME = "FT", "Fulltime"
    PARTTIME = "PT", "Parttime"
    CONTRACT = "CO", "Contract"
    SECONDMENT = "SE", "Secondment"
