from rest_framework import serializers
from django.contrib.auth import get_user_model
from OriginalPoint.models import Wallet

User = get_user_model()


class WalletCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
