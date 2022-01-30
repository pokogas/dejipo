# Generated by Django 3.2.9 on 2022-01-11 07:26

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('OriginalPoint', '0003_wallet_total_get_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('use_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('use_usage', models.IntegerField(choices=[(1, '支払い'), (2, '追加')], default=1)),
                ('status', models.IntegerField(choices=[(1, '完了'), (2, '未支払い'), (3, '発行済み')], default=1)),
                ('point', models.FloatField(default=0)),
                ('trading_time', models.DateTimeField(default=datetime.datetime(2022, 1, 11, 7, 26, 58, 885855, tzinfo=utc))),
                ('op', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OriginalPoint.originalpoint')),
                ('wallet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OriginalPoint.wallet')),
            ],
        ),
    ]