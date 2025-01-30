# Generated by Django 5.1.1 on 2025-01-30 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('core', '0001_initial'),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interview_round', models.IntegerField(default=1)),
                ('round', models.IntegerField(default=1)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('post_code', models.CharField(blank=True, max_length=10, null=True)),
                ('building', models.CharField(blank=True, max_length=20, null=True)),
                ('street', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('region', models.CharField(blank=True, max_length=20, null=True)),
                ('meeting_url', models.URLField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.country')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='jobs.job')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
    ]
