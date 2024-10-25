# Generated by Django 5.1.1 on 2024-10-23 08:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_remove_boards_columns_columns_board_jobs_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='columns',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='jobs.boards'),
        ),
        migrations.AlterUniqueTogether(
            name='columns',
            unique_together={('board', 'name', 'position')},
        ),
    ]
