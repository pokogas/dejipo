# Generated by Django 3.2.9 on 2022-01-11 07:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='trading_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
