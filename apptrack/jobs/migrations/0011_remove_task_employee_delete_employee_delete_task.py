# Generated by Django 5.1.1 on 2024-10-07 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_employee_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='employee',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
