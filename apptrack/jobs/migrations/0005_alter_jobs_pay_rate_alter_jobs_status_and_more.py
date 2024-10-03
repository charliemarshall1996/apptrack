# Generated by Django 5.1.1 on 2024-10-03 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_alter_jobs_location_delete_locations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='pay_rate',
            field=models.CharField(choices=[('unknown', 'unknown'), ('hourly', 'hourly'), ('daily', 'daily'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('yearly', 'yearly')], max_length=100),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='status',
            field=models.CharField(choices=[('archived', 'archived'), ('applied', 'applied'), ('rejected', 'rejected'), ('shortlisted', 'shortlisted'), ('interview', 'interview'), ('offer', 'offer'), ('open', 'open'), ('closed', 'closed')], max_length=100),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='work_contract',
            field=models.CharField(choices=[('unknown', 'unknown'), ('fulltime', 'fulltime'), ('parttime', 'parttime'), ('contract', 'contract'), ('secondment', 'secondment')], max_length=100),
        ),
    ]
