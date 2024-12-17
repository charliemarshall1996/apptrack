# Generated by Django 5.1.1 on 2024-12-17 21:20

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('summary', models.TextField()),
                ('published', models.DateTimeField()),
            ],
            options={
                'ordering': ['-published'],
            },
        ),
    ]
