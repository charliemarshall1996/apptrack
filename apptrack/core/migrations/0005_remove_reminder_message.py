# Generated by Django 5.1.1 on 2024-12-06 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_reminder_offset_reminder_offset_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reminder',
            name='message',
        ),
    ]