from rest_framework import serializers
from django.contrib.auth import get_user_model
from OriginalPoint.models import Wallet, OriginalPoint

User = get_user_model()


# オリジナルポイントリスト
class OriginalPointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginalPoint
        fields = (
            'id',
            'name',
            'pay_back_rate',
            'cost',
            'detailed_name',
            'introduction',
        )


# ウォレットリスト
class WalletListSerializer(serializers.ModelSerializer):
    op = OriginalPointListSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = (
            'id',
            'op',
            'point',
            'user'
        )


# ウォレット詳細
class WalletDetailSerializer(serializers.ModelSerializer):
    op = OriginalPointListSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = (
            'id',
            'op',
            'point',
            'user',
            'total_get_point'
        )
