import django_filters.rest_framework
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics, status, response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import TransactionListSerializer
from .models import Transaction
from rest_framework.response import Response
from OriginalPoint.models import Wallet, OpEntryUser
from django.utils import timezone
from rest_framework import pagination


# ページネーション設定
class TransactionListPagination(pagination.PageNumberPagination):
    page_size = 50


# ページネーション設定
class TransactionEachWalletListPagination(pagination.PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'next_count': self.page.number + 1,
            'results': data,
        })


# ユーザーが持ってるウォレットのトランザクションを全て取得
class UserTransactionList(generics.ListAPIView):
    serializer_class = TransactionListSerializer
    pagination_class = TransactionListPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        # リクエストしてきたuserの情報を変数userに格納
        user = self.request.user
        # userが持っているウォレットを取得
        wallets = Wallet.objects.filter(user=user)
        wallet_filter = []
        # forで繰り返しwallet_filterにwallet.idを追加していく。
        for wallet in wallets:
            wallet_filter.append(str(wallet.id))
        # トランザクションモデルからwallet_filterの中から新しい順でトランザクションを取得.order_by("-trading_time")
        return Transaction.objects.filter(
            wallet__in=wallet_filter).order_by("-trading_time")


# ユーザーが持っている指定したOPのウォレットのトランザクションを取得
class TransactionEachWalletList(generics.ListAPIView):
    pagination_class = TransactionEachWalletListPagination
    serializer_class = TransactionListSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        # リクエストしてきたuserの情報を変数userに格納
        user = self.request.user
        # op_nameパラメーターを変数op_nameに格納
        op_name = self.request.query_params.get("op_name")
        try:
            # ウォレットモデルにuserとop__nameが合致するものを変数walletに格納
            wallet = Wallet.objects.get(user=user, op__name=op_name)
            # トランザクションモデルからwalletの中から新しい順でトランザクションを取得.order_by("-trading_time")
            return Transaction.objects.filter(
                wallet=wallet).order_by("-trading_time")
        # ウォレットモデルにuserとop__nameが合致するものが見つからなかった場合
        except Wallet.DoesNotExist:
            return


@api_view(["GET", "POST"])
# GET(読み取り)未認証でもアクセス可能とする
@permission_classes((IsAuthenticatedOrReadOnly,))
def detail(request):
    # リクエストしてきたuserの情報を変数userに格納
    user = request.user
    try:
        # idパラメーターを変数transaction_idに格納
        transaction_id = request.query_params.get("id")
        # トランザクションモデルからtransaction_idと合致するものを変数transactionに格納
        transaction = Transaction.objects.get(id=transaction_id)
        # 経過時間をelapsed_timeに格納
        elapsed_time = timezone.now() - transaction.use_time
        # 経過時間が1800秒(30分)を過ぎていた場合
        if elapsed_time.seconds >= 1800:
            res = {"result": "NO", "detail": "利用期限切れのトランザクションです。"}
            return Response(res)
        # トランザクションのステータスが1(完了)になっていた場合
        if transaction.status == 1:
            res = {"result": "NO", "detail": "存在しないか利用できないトランザクションです。"}
            return Response(res)
        # opが招待制の場合
        if not transaction.op.publishing:
            # ユーザーが未認証の場合
            if user.is_anonymous:
                res = {"result": "NO", "detail": "招待制のトランザクションです。"}
                return Response(res)
            else:
                try:
                    # 招待済みユーザーの確認はuser・op・is_activeが合致した場合
                    OpEntryUser.objects.get(user=user, op=transaction.op, is_active=True)
                # user・op・is_activeが合致しない場合
                except OpEntryUser.DoesNotExist:
                    return Response({"result": "NO", "detail": "招待制のトランザクションです。"})
    # transaction_idが見つからない場合
    except Transaction.DoesNotExist:
        res = {"result": "NO", "detail": "存在しないか利用できないトランザクションです。"}
        return Response(res)
    # transaction_idはuuidの為形式がおかしい場合
    except ValidationError:
        res = {"result": "NO", "detail": "トランザクションIDが無効な形式です。"}
        return Response(res)
    # GETの場合
    if request.method == 'GET':
        context = {
            "id": transaction.id,
            "op_name": transaction.op.name,
            "op_id": transaction.op.id,
            "usage": transaction.use_usage,
            "time": transaction.use_time,
            "point": transaction.point
        }
        res = {"result": "OK", "detail": context}
        return Response(res, status=status.HTTP_200_OK)
    # POSTの場合
    elif request.method == 'POST':
        context = []
        # 再度確認
        try:
            wallet = Wallet.objects.get(user=user, op=transaction.op)
            if not transaction.op.publishing:
                try:
                    OpEntryUser.objects.get(user=user, op=transaction.op, is_active=True)
                except OpEntryUser.DoesNotExist:
                    return Response({"result": "NO", "detail": "招待されていないユーザーです"})
        except Wallet.DoesNotExist:
            return Response({"result": "NO", "detail": "ウォレットを所持していません"})
        # 支払いの場合
        if transaction.use_usage == 1:
            # ポイントが不足している場合
            if wallet.point < transaction.point:
                return Response({"result": "NO", "detail": "ウォレットのポイントが不足してます"})
            wallet.point -= transaction.point
            wallet.save()
            transaction.trading_time = timezone.now()
            transaction.wallet = wallet
            transaction.status = 1
            transaction.save()
            context = {"op_name": transaction.op.name, "point": transaction.point}
        # 付与の場合
        elif transaction.use_usage == 2:
            wallet.point += transaction.point
            wallet.total_get_point += transaction.point
            wallet.save()
            transaction.trading_time = timezone.now()
            transaction.wallet = wallet
            transaction.status = 1
            transaction.save()

            context = {"op_name": transaction.op.name, "point": transaction.point}
        return Response({"result": "OK", "detail": context}, status=status.HTTP_201_CREATED)
