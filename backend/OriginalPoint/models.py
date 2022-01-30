from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from Account.models import UserAccount
import uuid


class OriginalPoint(models.Model):
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', '半角英字のみ使用可能です')
    name = models.CharField(unique=True, max_length=10, validators=[alphanumeric, MinLengthValidator(3)])
    pay_back_rate = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    detailed_name = models.CharField(max_length=50)
    introduction = models.TextField(max_length=800)
    event = models.JSONField(blank=True, null=True)
    user_count = models.IntegerField(default=0)
    total_issuing_number = models.IntegerField(default=0)
    publishing = models.BooleanField(default=False)


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    op = models.ForeignKey(OriginalPoint, on_delete=models.CASCADE, blank=True, null=True)
    point = models.FloatField(default=0)
    total_get_point = models.FloatField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "op"],
                name="wallet_unique"
            ),
        ]


class OpEntryUser(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    op = models.ForeignKey(OriginalPoint, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "op"],
                name="op_entry_user_unique"
            ),
        ]
