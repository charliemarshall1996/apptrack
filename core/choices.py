import unicodedata

import pycountry


def normalize_country_name(name):
    return "".join(
        c for c in unicodedata.normalize("NFD", name) if unicodedata.category(c) != "Mn"
    ).strip()


def get_country_choices():
    country_choices = []
    countries = list(pycountry.countries)

    country_choices = [
        (country.alpha_2, normalize_country_name(country.name)) for country in countries
    ]

    return sorted(country_choices, key=lambda x: x[1])


def get_currency_choices():
    currency_choices = []
    currencies = list(pycountry.currencies)

    currency_choices = [(currency.alpha_3, currency.name) for currency in currencies]

    return sorted(currency_choices, key=lambda x: x[1])


class ChoiceBase:
    @classmethod
    def choices(cls):
        # Filter attributes that are tuples of length 2 (value and label)
        return [
            (value[0], value[1])
            for value in cls.__dict__.values()
            if isinstance(value, tuple) and len(value) == 2
        ]


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


class StatusChoices(ChoiceBase):
    OPEN = "OP", "Open"
    APPLIED = "AP", "Applied"
    REJECTED = "RE", "Rejected"
    SHORTLISTED = "SL", "Shortlisted"
    INTERVIEW = "IN", "Interview"
    OFFER = "OF", "Offer"
    CLOSED = "CL", "Closed"

    STATUS_NAMES = {
        OPEN[0]: OPEN[1],
        APPLIED[0]: APPLIED[1],
        REJECTED[0]: REJECTED[1],
        SHORTLISTED[0]: SHORTLISTED[1],
        INTERVIEW[0]: INTERVIEW[1],
        OFFER[0]: OFFER[1],
        CLOSED[0]: CLOSED[1],
    }

    STATUS_COLUMNS = {
        OPEN[0]: 1,
        APPLIED[0]: 2,
        SHORTLISTED[0]: 3,
        INTERVIEW[0]: 4,
        OFFER[0]: 5,
        REJECTED[0]: 6,
        CLOSED[0]: 7,
    }

    COLUMN_STATUSES = {
        1: OPEN,
        2: APPLIED,
        3: SHORTLISTED,
        4: INTERVIEW,
        5: OFFER,
        6: REJECTED,
        7: CLOSED,
    }

    APPLIED_STATUSES = [APPLIED[0], SHORTLISTED[0], INTERVIEW[0], OFFER[0], REJECTED[0]]

    @classmethod
    def get_status_column_position(cls, status):
        return cls.STATUS_COLUMNS[status]

    @classmethod
    def get_column_position_status(cls, position: int):
        return cls.COLUMN_STATUSES[position][0]

    @classmethod
    def get_column_position_status_name(cls, position: int):
        return cls.COLUMN_STATUSES[position][1]

    @classmethod
    def get_status_name(cls, status):
        return cls.STATUS_NAMES[status]

    @classmethod
    def get_applied_statuses(cls):
        return cls.APPLIED_STATUSES

    @classmethod
    def default(cls):
        return cls.OPEN[0]


class JobFunctionChoices(ChoiceBase):
    AA = "AA", "Accounting Assistant"
    AC = "AC", "Accounting Clerk"
    AD = "AD", "Accounting Director"
    APC = "APC", "Accounts Payable Clerk"
    APS = "APS", "Accounts Payable Specialist"
    ARC = "ARC", "Accounts Receivable Clerk"
    AE = "AE", "Account Executive"
    AM = "AM", "Account Manager"
    ACT = "ACT", "Actor"
    AT = "AT", "Actuary"
    AA2 = "AA2", "Administrative Assistant"
    AC2 = "AC2", "Admissions Coordinator"
    AE2 = "AE2", "Aircraft Electrician"
    AI = "AI", "Aircraft Inspector"
    AP = "AP", "Aircraft Painter"
    ASE = "ASE", "Application Security Engineer"
    AP3 = "AP3", "Appraiser"
    AR = "AR", "Archaeologist"
    A = "A", "Architect"
    APM = "APM", "Architectural Project Manager"
    ART = "ART", "Artist"
    AD2 = "AD2", "Art Director"
    AS = "AS", "Assembler"
    A2 = "A2", "Assistant Construction Superintendent"
    AC3 = "AC3", "Assistant Controller"
    AT2 = "AT2", "Athletic Trainer"
    AU = "AU", "Auditor"
    AD4 = "AD4", "AutoCAD Designer"
    AEM = "AEM", "Aviation Engine Mechanic"
    AST = "AST", "Aviation Service Technician"
    AT2 = "AT2", "Avionics Technician"
    BD = "BD", "Backend Developer"
    BA = "BA", "Bankruptcy Attorney"
    BT = "BT", "Bank Teller"
    BA2 = "BA2", "Behavior Analyst"
    BEA = "BEA", "Benefits Analyst"
    BES = "BES", "Benefits Specialist"
    BDE = "BDE", "Big Data Engineer"
    BS = "BS", "Billing Specialist"
    BM = "BM", "BIM Modeler"
    BSA = "BSA", "Biostatistician"
    BIA = "BIA", "BI Analyst"
    BID = "BID", "BI Developer"
    BK = "BK", "Bookkeeper"
    BA3 = "BA3", "Brand Ambassador"
    BM2 = "BM2", "Brand Manager"
    BM3 = "BM3", "Budget Manager"
    BA3 = "BA3", "Business Analyst"
    BDM = "BDM", "Business Development Manager"
    BSA2 = "BSA2", "Business Systems Analyst"
    CI = "CI", "Cable Installer"
    CD = "CD", "CAD Drafter"
    CCE = "CCE", "Call Center Data Entry Specialist"
    CCM = "CCM", "Call Center Manager"
    CCR = "CCR", "Call Center Representative"
    C = "C", "Caregiver"
    CEO2 = "CEO2", "CEO"
    CNA = "CNA", "Certified Nursing Assistant"
    CRNA = "CRNA", "Certified Registered Nurse Anesthetist"
    CRT = "CRT", "Certified Respiratory Therapist"
    CE = "CE", "Chemical Engineer"
    CFO = "CFO", "Chief Financial Officer"
    CHRO = "CHRO", "Chief Human Resources Officer"
    CIO = "CIO", "Chief Information Officer"
    CISO = "CISO", "Chief Information Security Officer"
    CMO = "CMO", "Chief Marketing Officer"
    COS = "COS", "Chief of Staff"
    COO = "COO", "Chief Operating Officer"
    CTO = "CTO", "Chief Technology Officer"
    CE2 = "CE2", "Civil Engineer"
    CA = "CA", "Claims Adjuster"
    CDM = "CDM", "Clinical Data Manager"
    CA2 = "CA2", "Cloud Architect"
    CM = "CM", "CNC Machinist"
    CR = "CR", "Collections Representative"
    CS = "CS", "Collections Specialist"
    CD2 = "CD2", "Communications Director"
    CM2 = "CM2", "Community Manager"
    CRC = "CRC", "Community Relations Coordinator"
    CA3 = "CA3", "Compensation Analyst"
    CM3 = "CM3", "Composite Mechanic"
    CA4 = "CA4", "Computer Analyst"
    CP = "CP", "Computer Programmer"
    CS2 = "CS2", "Computer Scientist"
    CON = "CON", "Concierge"
    CF = "CF", "Construction Foreman"
    CM4 = "CM4", "Construction Manager"
    CPC = "CPC", "Construction Project Captain"
    CPM = "CPM", "Construction Project Manager"
    CS2 = "CS2", "Construction Scheduler"
    CSM = "CSM", "Construction Superintendent"
    CP2 = "CP2", "Construction Vice President"
    CA5 = "CA5", "Contract Administrator"
    CA6 = "CA6", "Contract Attorney"
    CN = "CN", "Contract Negotiator"
    CTRL = "CTRL", "Controller"
    CW = "CW", "Copywriter"
    CC = "CC", "Corporate Counsel"
    CR2 = "CR2", "Corporate Recruiter"
    CE2 = "CE2", "Cost Estimator"
    CD3 = "CD3", "Creative Director"
    CS3 = "CS3", "Credentialing Specialist"
    CS4 = "CS4", "Credit Specialist"
    CRM = "CRM", "CRM Specialist"
    CSD = "CSD", "Customer Service Director"
    CSM2 = "CSM2", "Customer Service Manager"
    CA5 = "CA5", "Cybersecurity Analyst"
    C2 = "C2", "C++ Developer"
    DA = "DA", "Database Administrator"
    DA2 = "DA2", "Database Architect"
    DD = "DD", "Database Developer"
    DA3 = "DA3", "Data Analyst"
    DA4 = "DA4", "Data Architect"
    DE = "DE", "Data Engineer"
    DEC = "DEC", "Data Entry Clerk"
    DS = "DS", "Data Scientist"
    DD2 = "DD2", "Delivery Driver"
    DA5 = "DA5", "Dental Assistant"
    DH = "DH", "Dental Hygienist"
    DST = "DST", "Desktop Support Technician"
    DO = "DO", "DevOps Engineer"
    DA6 = "DA6", "Dialer Administrator"
    D2 = "D2", "Dietary Aide"
    DMA = "DMA", "Digital Marketing Analyst"
    DMM = "DMM", "Digital Marketing Manager"
    DH2 = "DH2", "Director of Housekeeping"
    DO2 = "DO2", "Director of Operations"
    D = "D", "Dispatcher"
    DCS = "DCS", "Document Control Specialist"
    DP = "DP", "Drone Pilot"
    DD3 = "DD3", "Drupal Developer"
    EE = "EE", "Electrical Engineer"
    EL = "EL", "Electrician"
    ET = "ET", "Electronics Technician"
    EMT = "EMT", "Electro-Mechanical Technician"
    EMS = "EMS", "Email Marketing Specialist"
    EMT2 = "EMT2", "Emergency Medical Technician (EMT)"
    ES = "ES", "Enrollment Specialist"
    EA = "EA", "Enterprise Architect"
    ESS = "ESS", "Enterprise Software Sales"
    EE2 = "EE2", "Environmental Engineer"
    EFS = "EFS", "Environmental Field Technician"
    ES2 = "ES2", "Environmental Scientist"
    EPA = "EPA", "Estate Planning Attorney"
    EST = "EST", "Esthetician"
    ED = "ED", "ETL Developer"
    EC = "EC", "Event Coordinator"
    EP = "EP", "Event Planner"
    EA2 = "EA2", "Executive Assistant"
    ED2 = "ED2", "E-Discovery Professional"
    FM = "FM", "Facilities Manager"
    FA = "FA", "Family Attorney"
    FC = "FC", "File Clerk"
    FD = "FD", "Finance Director"
    FA2 = "FA2", "Financial Advisor"
    FA3 = "FA3", "Financial Aid Specialist"
    FA4 = "FA4", "Financial Analyst"
    FM2 = "FM2", "Financial Manager"
    FA5 = "FA5", "Flight Attendant"
    FO = "FO", "Forklift Operator"
    FED = "FED", "Front End Developer"
    FC2 = "FC2", "Fulfillment Coordinator"
    FSD = "FSD", "Full Stack Developer"
    GD = "GD", "Game Designer"
    GC = "GC", "Garbage Collector"
    GM = "GM", "General Manager"
    GEO = "GEO", "Geologist"
    GE = "GE", "Geotechnical Engineer"
    GIS = "GIS", "GIS Specialist"
    GW = "GW", "Grant Writer"
    GD2 = "GD2", "Graphic Designer"
    HCC = "HCC", "Healthcare Customer Care Representative"
    HES = "HES", "Healthcare Enrollment Specialist"
    HEP = "HEP", "Healthcare Project Manager"
    HR = "HR", "HR Generalist"
    HRM = "HRM", "HR Manager"
    HRBP = "HRBP", "HR Business Partner"
    HRO = "HRO", "HR Operations Specialist"
    HRC = "HRC", "Human Resource Consultant"
    HIR = "HIR", "Human Resources Coordinator"
    IT = "IT", "Information Technology Manager"
    IS = "IS", "IT Specialist"
    IA = "IA", "IT Administrator"
    IM = "IM", "IT Manager"
    IS2 = "IS2", "IT Support Specialist"
    JD = "JD", "Java Developer"
    JSM = "JSM", "JavaScript Manager"
    JSP = "JSP", "JavaScript Programmer"
    JSE = "JSE", "JavaScript Engineer"
    LSA = "LSA", "Laboratory Assistant"
    LA = "LA", "Lawyer"
    LM = "LM", "Legal Manager"
    LPR = "LPR", "Legal Paralegal"
    LO = "LO", "Legal Officer"
    LM2 = "LM2", "Legal Marketing Specialist"
    LAM = "LAM", "Legal Assistant Manager"
    MD = "MD", "Medical Doctor"
    MDA = "MDA", "Medical Assistant"
    MDS = "MDS", "Medical Data Specialist"
    MEC = "MEC", "Medical Equipment Coordinator"
    MT = "MT", "Medical Technician"
    ME = "ME", "Mechanical Engineer"
    MEP = "MEP", "Mechanical Engineer Project Manager"
    MFE = "MFE", "Manufacturing Engineer"
    MFP = "MFP", "Manufacturing Process Engineer"
    MEX = "MEX", "Merchandiser"
    MEX2 = "MEX2", "Marketing Executive"
    MKD = "MKD", "Marketing Director"
    MSO = "MSO", "Marketing and Sales Officer"
    MS = "MS", "Marketing Specialist"
    MS2 = "MS2", "Market Research Specialist"
    MO = "MO", "Math Olympiad Coach"
    MC = "MC", "Mobile Developer"
    ME2 = "ME2", "Machine Engineer"
    M2 = "M2", "Mail Clerk"
    MGR = "MGR", "Manager"
    MN = "MN", "Manual Labor"
    MB = "MB", "Merchandising Buyer"
    MM = "MM", "Materials Manager"
    MPA = "MPA", "Medical Physicist"
    M2 = "M2", "Maintenance Technician"
    M4 = "M4", "Maintenance Manager"
    M5 = "M5", "Machine Shop Supervisor"
    MG = "MG", "Marketing Generalist"
    NS = "NS", "Nurse"
    NC = "NC", "Network Consultant"
    NR = "NR", "Nurse"
    ND = "ND", "Network Developer"
    NOS = "NOS", "Network Operations Specialist"
    NT = "NT", "Nurse Practitioner"
    NT2 = "NT2", "Nurse Technician"
    OTR = "OTR", "Operations Team Representative"
    OSE = "OSE", "Operations Support Engineer"
    OPA = "OPA", "Operations Assistant"
    OP = "OP", "Operator"
    OS = "OS", "Operations Specialist"
    PAF = "PAF", "Program Analyst"
    PA2 = "PA2", "Project Assistant"
    PF = "PF", "Project Facilitator"
    PMO = "PMO", "Project Manager"
    PD = "PD", "Product Designer"
    PP = "PP", "Procurement Specialist"
    PSC = "PSC", "Patient Services Coordinator"
    PS = "PS", "Project Support"
    QA = "QA", "Quality Analyst"
    QP = "QP", "Quality Assurance"
    QA2 = "QA2", "Quality Assurance Manager"
    QA3 = "QA3", "Quality Assurance Specialist"
    RA = "RA", "Research Assistant"
    RD = "RD", "Research Director"
    RE = "RE", "Research Engineer"
    RN = "RN", "Researcher"
    RM = "RM", "Recruitment Manager"
    RE2 = "RE2", "Recruitment Executive"
    RN2 = "RN2", "Regional Nurse"
    RO = "RO", "Risk Officer"
    RSE = "RSE", "Regulatory Specialist"
    RAE = "RAE", "Risk Assessment Expert"
    SC = "SC", "Software Consultant"
    SDE = "SDE", "Software Development Engineer"
    SE = "SE", "Software Engineer"
    SS = "SS", "Security Specialist"
    SA = "SA", "Sales Associate"
    SMA = "SMA", "Sales Manager"
    SR = "SR", "Sales Representative"
    SAE = "SAE", "Sales Executive"
    SEM = "SEM", "Search Engine Marketer"
    SMA2 = "SMA2", "Senior Marketing Analyst"
    SSE = "SSE", "Senior Software Engineer"
    SD2 = "SD2", "Senior Developer"
    SM2 = "SM2", "Senior Manager"
    SN = "SN", "Senior Nurse"
    SPM = "SPM", "Senior Project Manager"
    SO = "SO", "Security Officer"
    SPA = "SPA", "Security Analyst"
    SD3 = "SD3", "System Developer"
    SUP = "SUP", "Supervisor"
    SVP = "SVP", "Senior Vice President"
    SW = "SW", "Software Writer"
    TC = "TC", "Technical Consultant"
    TFA = "TFA", "Technical Field Advisor"
    TSE = "TSE", "Technical Support Engineer"
    TSM = "TSM", "Technical Support Manager"
    TL = "TL", "Team Leader"
    TO = "TO", "Technical Officer"
    TS = "TS", "Technical Specialist"
    UAM = "UAM", "Urban Affairs Manager"
    UM = "UM", "User Manager"
    UI = "UI", "User Interface Designer"
    UX = "UX", "User Experience Designer"
    VA = "VA", "Virtual Assistant"
    VPM = "VPM", "Vice President of Marketing"
    VP = "VP", "Vice President"
    VPL = "VPL", "Vice President of Logistics"
    WM = "WM", "Warehouse Manager"
    WES = "WES", "Warehouse Executive"
    WPC = "WPC", "Warehouse Picker"
    WPL = "WPL", "Warehouse Planner"
    WPS = "WPS", "Warehouse Supervisor"
    WR = "WR", "Web Developer"
    WSE = "WSE", "Web Software Engineer"
    WSC = "WSC", "Web Services Consultant"
    WS = "WS", "Web Specialist"
    WP = "WP", "Web Programmer"
    WEM = "WEM", "Web Manager"
    WD = "WD", "Web Designer"
    WSE2 = "WSE2", "Web Support Engineer"
    WSE3 = "WSE3", "Web Systems Engineer"
    XS = "XS", "X-Ray Specialist"
    YM = "YM", "Youth Mentor"
    ZM = "ZM", "Zoologist"


class PayRateChoices(ChoiceBase):
    UNKNOWN = "UK", "Unknown"
    HOURLY = "HR", "Hourly"
    DAILY = "DY", "Daily"
    WEEKLY = "WK", "Weekly"
    MONTHLY = "MO", "Monthly"
    YEARLY = "YR", "Yearly"


class ReminderUnitChoices(ChoiceBase):
    DAYS = "d", "Days"
    HOURS = "h", "Hours"
    MINUTES = "m", "Minutes"
