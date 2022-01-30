import uuid
from django.db import models
from django.utils import timezone

from OriginalPoint.models import OriginalPoint, Wallet


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    use_time = models.DateTimeField(default=timezone.now)
    use_usage_count = (
        (1, '支払い'),
        (2, '追加'),
    )
    use_usage = models.IntegerField(choices=use_usage_count, default=1)
    status_count = (
        (1, '完了'),
        (2, '未支払い'),
        (3, '発行済み'),
    )
    status = models.IntegerField(choices=status_count, default=1)
    op = models.ForeignKey(OriginalPoint, on_delete=models.CASCADE, blank=True, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True, null=True)
    point = models.FloatField(default=0)
    trading_time = models.DateTimeField(default=timezone.now)
