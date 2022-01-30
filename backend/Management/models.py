import uuid
from django.utils import timezone
from django.db import models
from Account.models import UserAccount
from OriginalPoint.models import OriginalPoint


class OpManagement(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    op = models.ForeignKey(OriginalPoint, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    permission_level_count = (
        (1, 'Admin'),
        (2, 'staff'),
    )
    permission_level = models.IntegerField(choices=permission_level_count, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "op"],
                name="op_manage_unique"
            ),
        ]


class OpInvitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    use_time = models.DateTimeField(default=timezone.now)
    time_limit = models.IntegerField(default=0)
    op = models.ForeignKey(OriginalPoint, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    use_limit_c = models.IntegerField(default=0)
    using_c = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["op"],
                name="op_invite_ation_unique"
            ),
        ]
