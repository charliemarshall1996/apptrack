# Generated by Django 5.1.1 on 2024-12-10 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streak',
            name='current_streak_start',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]