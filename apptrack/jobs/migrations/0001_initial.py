# Generated by Django 5.1.1 on 2024-10-03 15:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('url', models.URLField(blank=True, null=True)),
                ('source', models.CharField(choices=[('WW', 'Web'), ('HH', 'Headhunter'), ('NP', 'Newspaper'), ('CW', 'Company Website'), ('RF', 'Referral'), ('JB', 'Job Board'), ('RA', 'Recruitment Agency'), ('SM', 'Social Media'), ('CF', 'Career Fair'), ('IP', 'Internal Posting'), ('FP', 'Freelance Platform'), ('UC', 'University Career Services'), ('NE', 'Networking Event'), ('PA', 'Professional Association'), ('GP', 'Government Job Portal'), ('CO', 'Cold Outreach'), ('JN', 'Job Newsletter'), ('FN', 'Freelancer Network')], max_length=2)),
                ('job_title', models.CharField(max_length=100)),
                ('job_function', models.CharField(blank=True, choices=[('AC', 'Accounting'), ('AD', 'Advertising'), ('AE', 'Aerospace Engineering'), ('AG', 'Agriculture'), ('AR', 'Architecture'), ('AU', 'Automotive Engineering'), ('AV', 'Aviation'), ('BA', 'Banking'), ('BI', 'Biotechnology'), ('BM', 'Broadcast Media'), ('BD', 'Business Development'), ('BO', 'Business Operations'), ('CE', 'Chemical Engineering'), ('CO', 'Computer Engineering'), ('CM', 'Construction Management'), ('CN', 'Consulting'), ('CS', 'Customer Service'), ('DS', 'Data Science'), ('DE', 'Design'), ('ED', 'Education'), ('EE', 'Electrical Engineering'), ('EN', 'Energy'), ('EG', 'Engineering'), ('ET', 'Entertainment'), ('ES', 'Environmental Science'), ('FI', 'Finance'), ('FS', 'Food Services'), ('GO', 'Government'), ('HE', 'Healthcare'), ('HR', 'Human Resources'), ('IT', 'Information Technology'), ('IN', 'Insurance'), ('IB', 'Investment Banking'), ('LE', 'Legal'), ('LO', 'Logistics'), ('MF', 'Manufacturing'), ('MK', 'Marketing'), ('MD', 'Media'), ('ME', 'Medical Devices'), ('MI', 'Mining'), ('NP', 'Non-profit'), ('PH', 'Pharmaceuticals'), ('PR', 'Public Relations'), ('PM', 'Project Management'), ('RE', 'Real Estate'), ('RC', 'Recruiting'), ('RT', 'Retail'), ('SA', 'Sales'), ('SP', 'Sports'), ('SC', 'Supply Chain'), ('TS', 'Technical Support'), ('TC', 'Telecommunications'), ('TR', 'Transportation'), ('TT', 'Travel & Tourism'), ('UT', 'Utilities'), ('VC', 'Venture Capital'), ('WH', 'Wholesale'), ('OT', 'Other')], max_length=2, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('location_policy', models.CharField(blank=True, choices=[('UK', 'Unknown'), ('HY', 'Hybrid'), ('ON', 'On-Site'), ('RE', 'Remote'), ('FL', 'Flexible')], max_length=100, null=True)),
                ('work_contract', models.CharField(blank=True, choices=[('UK', 'Unknown'), ('FT', 'Fulltime'), ('PT', 'Parttime'), ('CO', 'Contract'), ('SE', 'Secondment')], max_length=100, null=True)),
                ('min_pay', models.IntegerField(blank=True, null=True)),
                ('max_pay', models.IntegerField(blank=True, null=True)),
                ('pay_rate', models.CharField(blank=True, choices=[('UK', 'Unknown'), ('HR', 'Hourly'), ('DY', 'Daily'), ('WK', 'Weekly'), ('MO', 'Monthly'), ('YR', 'Yearly')], max_length=100, null=True)),
                ('currency', models.CharField(blank=True, max_length=100, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('AP', 'applied'), ('RE', 'rejected'), ('SL', 'shortlisted'), ('IN', 'interview'), ('OF', 'offer'), ('OP', 'open'), ('CL', 'closed')], default='OP', max_length=3)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.locations')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
