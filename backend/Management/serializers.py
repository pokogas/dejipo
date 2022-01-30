from rest_framework import serializers
from django.contrib.auth import get_user_model

from Account.models import UserAccount
from OriginalPoint.models import OriginalPoint, Wallet
from .models import OpManagement
from Transaction.models import Transaction

User = get_user_model()


class OriginalPointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginalPoint
        fields = "__all__"


class UserManagementOpListSerializer(serializers.ModelSerializer):
    op = OriginalPointListSerializer(read_only=True)

    class Meta:
        model = OpManagement
        fields = (
            'id',
            'op',
            'is_active',
            'permission_level'
        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = (
            'name',
            'email',
            'id',
        )
