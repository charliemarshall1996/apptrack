# Generated by Django 5.1.1 on 2024-10-05 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_jobs_job_title_alter_jobs_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.columns'),
        ),
    ]
