# Generated by Django 5.1.1 on 2024-12-13 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_job_date_offered_set_job_offered'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobfunction',
            name='code',
            field=models.CharField(default='na', max_length=4),
            preserve_default=False,
        ),
    ]
