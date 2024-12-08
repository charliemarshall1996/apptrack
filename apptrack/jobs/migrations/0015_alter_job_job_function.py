# Generated by Django 5.1.1 on 2024-12-08 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_rename_town_job_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_function',
            field=models.CharField(blank=True, choices=[('AA', 'Accounting Assistant'), ('AC', 'Accounting Clerk'), ('AD', 'Accounting Director'), ('APC', 'Accounts Payable Clerk'), ('APS', 'Accounts Payable Specialist'), ('ARC', 'Accounts Receivable Clerk'), ('AE', 'Account Executive'), ('AM', 'Account Manager'), ('ACT', 'Actor'), ('AT', 'Actuary'), ('AA2', 'Administrative Assistant'), ('AC2', 'Admissions Coordinator'), ('AE2', 'Aircraft Electrician'), ('AI', 'Aircraft Inspector'), ('AP', 'Aircraft Painter'), ('ASE', 'Application Security Engineer'), ('AP3', 'Appraiser'), ('AR', 'Archaeologist'), ('A', 'Architect'), ('APM', 'Architectural Project Manager'), ('ART', 'Artist'), ('AD2', 'Art Director'), ('AS', 'Assembler'), ('A2', 'Assistant Construction Superintendent'), ('AC3', 'Assistant Controller'), ('AT2', 'Avionics Technician'), ('AU', 'Auditor'), ('AD4', 'AutoCAD Designer'), ('AEM', 'Aviation Engine Mechanic'), ('AST', 'Aviation Service Technician'), ('BD', 'Backend Developer'), ('BA', 'Bankruptcy Attorney'), ('BT', 'Bank Teller'), ('BA2', 'Behavior Analyst'), ('BEA', 'Benefits Analyst'), ('BES', 'Benefits Specialist'), ('BDE', 'Big Data Engineer'), ('BS', 'Billing Specialist'), ('BM', 'BIM Modeler'), ('BSA', 'Biostatistician'), ('BIA', 'BI Analyst'), ('BID', 'BI Developer'), ('BK', 'Bookkeeper'), ('BA3', 'Business Analyst'), ('BM2', 'Brand Manager'), ('BM3', 'Budget Manager'), ('BDM', 'Business Development Manager'), ('BSA2', 'Business Systems Analyst'), ('CI', 'Cable Installer'), ('CD', 'CAD Drafter'), ('CCE', 'Call Center Data Entry Specialist'), ('CCM', 'Call Center Manager'), ('CCR', 'Call Center Representative'), ('C', 'Caregiver'), ('CEO2', 'CEO'), ('CNA', 'Certified Nursing Assistant'), ('CRNA', 'Certified Registered Nurse Anesthetist'), ('CRT', 'Certified Respiratory Therapist'), ('CE', 'Chemical Engineer'), ('CFO', 'Chief Financial Officer'), ('CHRO', 'Chief Human Resources Officer'), ('CIO', 'Chief Information Officer'), ('CISO', 'Chief Information Security Officer'), ('CMO', 'Chief Marketing Officer'), ('COS', 'Chief of Staff'), ('COO', 'Chief Operating Officer'), ('CTO', 'Chief Technology Officer'), ('CE2', 'Cost Estimator'), ('CA', 'Claims Adjuster'), ('CDM', 'Clinical Data Manager'), ('CA2', 'Cloud Architect'), ('CM', 'CNC Machinist'), ('CR', 'Collections Representative'), ('CS', 'Collections Specialist'), ('CD2', 'Communications Director'), ('CM2', 'Community Manager'), ('CRC', 'Community Relations Coordinator'), ('CA3', 'Compensation Analyst'), ('CM3', 'Composite Mechanic'), ('CA4', 'Computer Analyst'), ('CP', 'Computer Programmer'), ('CS2', 'Construction Scheduler'), ('CON', 'Concierge'), ('CF', 'Construction Foreman'), ('CM4', 'Construction Manager'), ('CPC', 'Construction Project Captain'), ('CPM', 'Construction Project Manager'), ('CSM', 'Construction Superintendent'), ('CP2', 'Construction Vice President'), ('CA5', 'Cybersecurity Analyst'), ('CA6', 'Contract Attorney'), ('CN', 'Contract Negotiator'), ('CTRL', 'Controller'), ('CW', 'Copywriter'), ('CC', 'Corporate Counsel'), ('CR2', 'Corporate Recruiter'), ('CD3', 'Creative Director'), ('CS3', 'Credentialing Specialist'), ('CS4', 'Credit Specialist'), ('CRM', 'CRM Specialist'), ('CSD', 'Customer Service Director'), ('CSM2', 'Customer Service Manager'), ('C2', 'C++ Developer'), ('DA', 'Database Administrator'), ('DA2', 'Database Architect'), ('DD', 'Database Developer'), ('DA3', 'Data Analyst'), ('DA4', 'Data Architect'), ('DE', 'Data Engineer'), ('DEC', 'Data Entry Clerk'), ('DS', 'Data Scientist'), ('DD2', 'Delivery Driver'), ('DA5', 'Dental Assistant'), ('DH', 'Dental Hygienist'), ('DST', 'Desktop Support Technician'), ('DO', 'DevOps Engineer'), ('DA6', 'Dialer Administrator'), ('D2', 'Dietary Aide'), ('DMA', 'Digital Marketing Analyst'), ('DMM', 'Digital Marketing Manager'), ('DH2', 'Director of Housekeeping'), ('DO2', 'Director of Operations'), ('D', 'Dispatcher'), ('DCS', 'Document Control Specialist'), ('DP', 'Drone Pilot'), ('DD3', 'Drupal Developer'), ('EE', 'Electrical Engineer'), ('EL', 'Electrician'), ('ET', 'Electronics Technician'), ('EMT', 'Electro-Mechanical Technician'), ('EMS', 'Email Marketing Specialist'), ('EMT2', 'Emergency Medical Technician (EMT)'), ('ES', 'Enrollment Specialist'), ('EA', 'Enterprise Architect'), ('ESS', 'Enterprise Software Sales'), ('EE2', 'Environmental Engineer'), ('EFS', 'Environmental Field Technician'), ('ES2', 'Environmental Scientist'), ('EPA', 'Estate Planning Attorney'), ('EST', 'Esthetician'), ('ED', 'ETL Developer'), ('EC', 'Event Coordinator'), ('EP', 'Event Planner'), ('EA2', 'Executive Assistant'), ('ED2', 'E-Discovery Professional'), ('FM', 'Facilities Manager'), ('FA', 'Family Attorney'), ('FC', 'File Clerk'), ('FD', 'Finance Director'), ('FA2', 'Financial Advisor'), ('FA3', 'Financial Aid Specialist'), ('FA4', 'Financial Analyst'), ('FM2', 'Financial Manager'), ('FA5', 'Flight Attendant'), ('FO', 'Forklift Operator'), ('FED', 'Front End Developer'), ('FC2', 'Fulfillment Coordinator'), ('FSD', 'Full Stack Developer'), ('GD', 'Game Designer'), ('GC', 'Garbage Collector'), ('GM', 'General Manager'), ('GEO', 'Geologist'), ('GE', 'Geotechnical Engineer'), ('GIS', 'GIS Specialist'), ('GW', 'Grant Writer'), ('GD2', 'Graphic Designer'), ('HCC', 'Healthcare Customer Care Representative'), ('HES', 'Healthcare Enrollment Specialist'), ('HEP', 'Healthcare Project Manager'), ('HR', 'HR Generalist'), ('HRM', 'HR Manager'), ('HRBP', 'HR Business Partner'), ('HRO', 'HR Operations Specialist'), ('HRC', 'Human Resource Consultant'), ('HIR', 'Human Resources Coordinator'), ('IT', 'Information Technology Manager'), ('IS', 'IT Specialist'), ('IA', 'IT Administrator'), ('IM', 'IT Manager'), ('IS2', 'IT Support Specialist'), ('JD', 'Java Developer'), ('JSM', 'JavaScript Manager'), ('JSP', 'JavaScript Programmer'), ('JSE', 'JavaScript Engineer'), ('LSA', 'Laboratory Assistant'), ('LA', 'Lawyer'), ('LM', 'Legal Manager'), ('LPR', 'Legal Paralegal'), ('LO', 'Legal Officer'), ('LM2', 'Legal Marketing Specialist'), ('LAM', 'Legal Assistant Manager'), ('MD', 'Medical Doctor'), ('MDA', 'Medical Assistant'), ('MDS', 'Medical Data Specialist'), ('MEC', 'Medical Equipment Coordinator'), ('MT', 'Medical Technician'), ('ME', 'Mechanical Engineer'), ('MEP', 'Mechanical Engineer Project Manager'), ('MFE', 'Manufacturing Engineer'), ('MFP', 'Manufacturing Process Engineer'), ('MEX', 'Merchandiser'), ('MEX2', 'Marketing Executive'), ('MKD', 'Marketing Director'), ('MSO', 'Marketing and Sales Officer'), ('MS', 'Marketing Specialist'), ('MS2', 'Market Research Specialist'), ('MO', 'Math Olympiad Coach'), ('MC', 'Mobile Developer'), ('ME2', 'Machine Engineer'), ('M2', 'Maintenance Technician'), ('MGR', 'Manager'), ('MN', 'Manual Labor'), ('MB', 'Merchandising Buyer'), ('MM', 'Materials Manager'), ('MPA', 'Medical Physicist'), ('M4', 'Maintenance Manager'), ('M5', 'Machine Shop Supervisor'), ('MG', 'Marketing Generalist'), ('NS', 'Nurse'), ('NC', 'Network Consultant'), ('NR', 'Nurse'), ('ND', 'Network Developer'), ('NOS', 'Network Operations Specialist'), ('NT', 'Nurse Practitioner'), ('NT2', 'Nurse Technician'), ('OTR', 'Operations Team Representative'), ('OSE', 'Operations Support Engineer'), ('OPA', 'Operations Assistant'), ('OP', 'Operator'), ('OS', 'Operations Specialist'), ('PAF', 'Program Analyst'), ('PA2', 'Project Assistant'), ('PF', 'Project Facilitator'), ('PMO', 'Project Manager'), ('PD', 'Product Designer'), ('PP', 'Procurement Specialist'), ('PSC', 'Patient Services Coordinator'), ('PS', 'Project Support'), ('QA', 'Quality Analyst'), ('QP', 'Quality Assurance'), ('QA2', 'Quality Assurance Manager'), ('QA3', 'Quality Assurance Specialist'), ('RA', 'Research Assistant'), ('RD', 'Research Director'), ('RE', 'Research Engineer'), ('RN', 'Researcher'), ('RM', 'Recruitment Manager'), ('RE2', 'Recruitment Executive'), ('RN2', 'Regional Nurse'), ('RO', 'Risk Officer'), ('RSE', 'Regulatory Specialist'), ('RAE', 'Risk Assessment Expert'), ('SC', 'Software Consultant'), ('SDE', 'Software Development Engineer'), ('SE', 'Software Engineer'), ('SS', 'Security Specialist'), ('SA', 'Sales Associate'), ('SMA', 'Sales Manager'), ('SR', 'Sales Representative'), ('SAE', 'Sales Executive'), ('SEM', 'Search Engine Marketer'), ('SMA2', 'Senior Marketing Analyst'), ('SSE', 'Senior Software Engineer'), ('SD2', 'Senior Developer'), ('SM2', 'Senior Manager'), ('SN', 'Senior Nurse'), ('SPM', 'Senior Project Manager'), ('SO', 'Security Officer'), ('SPA', 'Security Analyst'), ('SD3', 'System Developer'), ('SUP', 'Supervisor'), ('SVP', 'Senior Vice President'), ('SW', 'Software Writer'), ('TC', 'Technical Consultant'), ('TFA', 'Technical Field Advisor'), ('TSE', 'Technical Support Engineer'), ('TSM', 'Technical Support Manager'), ('TL', 'Team Leader'), ('TO', 'Technical Officer'), ('TS', 'Technical Specialist'), ('UAM', 'Urban Affairs Manager'), ('UM', 'User Manager'), ('UI', 'User Interface Designer'), ('UX', 'User Experience Designer'), ('VA', 'Virtual Assistant'), ('VPM', 'Vice President of Marketing'), ('VP', 'Vice President'), ('VPL', 'Vice President of Logistics'), ('WM', 'Warehouse Manager'), ('WES', 'Warehouse Executive'), ('WPC', 'Warehouse Picker'), ('WPL', 'Warehouse Planner'), ('WPS', 'Warehouse Supervisor'), ('WR', 'Web Developer'), ('WSE', 'Web Software Engineer'), ('WSC', 'Web Services Consultant'), ('WS', 'Web Specialist'), ('WP', 'Web Programmer'), ('WEM', 'Web Manager'), ('WD', 'Web Designer'), ('WSE2', 'Web Support Engineer'), ('WSE3', 'Web Systems Engineer'), ('XS', 'X-Ray Specialist'), ('YM', 'Youth Mentor'), ('ZM', 'Zoologist')], max_length=4, null=True),
        ),
    ]
