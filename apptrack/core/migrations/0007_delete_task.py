# Generated by Django 5.1.1 on 2024-12-10 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_country_currency'),
        ('interview', '0002_delete_interviewtask'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Task',
        ),
    ]
