# Generated by Django 5.1.1 on 2024-12-13 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_interview_round'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationpolicy',
            name='code',
            field=models.CharField(default='na', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payrate',
            name='code',
            field=models.CharField(default='na', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workcontract',
            name='code',
            field=models.CharField(default='na', max_length=2),
            preserve_default=False,
        ),
    ]
