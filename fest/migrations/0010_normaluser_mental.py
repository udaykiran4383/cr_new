# Generated by Django 4.1 on 2023-01-18 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0009_remove_normaluser_menheal_normaluser_disable'),
    ]

    operations = [
        migrations.AddField(
            model_name='normaluser',
            name='mental',
            field=models.BooleanField(default=False, verbose_name='Ananya Birla'),
        ),
    ]
