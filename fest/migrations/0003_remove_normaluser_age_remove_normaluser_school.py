# Generated by Django 4.1 on 2023-01-08 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0002_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='normaluser',
            name='age',
        ),
        migrations.RemoveField(
            model_name='normaluser',
            name='school',
        ),
    ]
