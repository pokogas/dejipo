from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
import django_filters.rest_framework
from rest_framework.exceptions import APIException
from rest_framework import filters
from .serializers import WalletListSerializer, WalletDetailSerializer, OriginalPointListSerializer
from OriginalPoint.models import Wallet, OriginalPoint


class OriginalPointNotFound(APIException):
    status_code = 400
    default_detail = 'OriginalPointが見つかりませんでした。'
    default_code = 'OriginalPoint-not-found'


class WalletList(generics.ListAPIView):
    serializer_class = WalletListSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(user=user)


class WalletDetail(generics.ListAPIView):
    serializer_class = WalletDetailSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        op = self.request.query_params.get("op_name")
        # OPが見つからない場合場合OriginalPointNotFoundがResponseされる
        if len(OriginalPoint.objects.filter(name=op)) == 0:
            raise OriginalPointNotFound
        return Wallet.objects.filter(user=user, op__name=op)


class OriginalPointList(generics.ListAPIView):
    serializer_class = OriginalPointListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name']

    def get_queryset(self):
        return OriginalPoint.objects.filter(publishing=True)
