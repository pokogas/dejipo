from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Transaction
from OriginalPoint.models import OriginalPoint

User = get_user_model()


class OriginalPointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginalPoint
        fields = (
            'id',
            'name',
            'pay_back_rate',
            'cost',
        )


class TransactionListSerializer(serializers.ModelSerializer):
    op = OriginalPointListSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
