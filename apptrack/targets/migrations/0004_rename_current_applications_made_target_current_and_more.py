# Generated by Django 5.1.1 on 2024-12-10 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0003_alter_target_streak'),
    ]

    operations = [
        migrations.RenameField(
            model_name='target',
            old_name='current_applications_made',
            new_name='current',
        ),
        migrations.RenameField(
            model_name='target',
            old_name='target_applications_made',
            new_name='daily_target',
        ),
    ]
