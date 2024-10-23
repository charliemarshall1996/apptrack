# Generated by Django 5.1.1 on 2024-10-23 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boards',
            name='columns',
        ),
        migrations.AddField(
            model_name='columns',
            name='board',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jobs.boards'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobs',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='jobs.boards'),
        ),
    ]
