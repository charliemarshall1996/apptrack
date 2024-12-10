# Generated by Django 5.1.1 on 2024-12-09 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_streak_target_profile_current_applications_made_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streak',
            name='current_streak',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='streak',
            name='longest_streak',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]