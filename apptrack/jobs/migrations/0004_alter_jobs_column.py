# Generated by Django 5.1.1 on 2024-11-28 11:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_rename_company_name_jobs_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='column', to='jobs.columns'),
        ),
    ]