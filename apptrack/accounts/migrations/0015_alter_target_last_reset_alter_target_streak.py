# Generated by Django 5.1.1 on 2024-12-13 11:59

import django.db.models.deletion
import django.db.models.query
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_target_streak'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='last_reset',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='target',
            name='streak',
            field=models.ForeignKey(default=django.db.models.query.QuerySet.create, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target', to='accounts.streak'),
        ),
    ]
