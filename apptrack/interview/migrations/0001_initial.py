# Generated by Django 5.1.1 on 2024-12-02 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0010_alter_job_status_alter_job_updated'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interview_round', models.IntegerField(default=1)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('post_code', models.CharField(blank=True, max_length=10, null=True)),
                ('building', models.CharField(blank=True, max_length=20, null=True)),
                ('street', models.CharField(blank=True, max_length=20, null=True)),
                ('town', models.CharField(blank=True, max_length=20, null=True)),
                ('region', models.CharField(blank=True, max_length=20, null=True)),
                ('meeting_url', models.URLField(blank=True, null=True)),
                ('country', models.CharField(max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='jobs.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interviewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interview.interview')),
            ],
        ),
        migrations.CreateModel(
            name='InterviewTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_completed', models.BooleanField(default=False)),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='interview.interview')),
            ],
        ),
    ]
