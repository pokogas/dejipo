from django.core.exceptions import ValidationError
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
import django_filters.rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework import generics, pagination, response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from .serializers import UserManagementOpListSerializer, OriginalPointListSerializer, TransactionSerializer, \
    UserListSerializer
from OriginalPoint.models import OriginalPoint, OpEntryUser, Wallet
from .models import OpManagement, OpInvitation
from Transaction.models import Transaction
from rest_framework.response import Response
from django.db import IntegrityError
from Account.models import UserAccount


class TransactionListPagination(pagination.PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
            'page_size': self.page_size,
            'range_first': (self.page.number * self.page_size) - self.page_size + 1,
            'range_last': min((self.page.number * self.page_size), self.page.paginator.count),
        })


class UserListSerializerPagination(pagination.PageNumberPagination):
    page_size = 30

    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
            'page_size': self.page_size,
            'range_first': (self.page.number * self.page_size) - self.page_size + 1,
            'range_last': min((self.page.number * self.page_size), self.page.paginator.count),
        })


class OriginalPointNotFound(APIException):
    status_code = 400
    default_detail = 'OriginalPointが見つかりませんでした。'
    default_code = 'OriginalPoint-not-found'


class OptionNotFound(APIException):
    status_code = 400
    default_detail = 'optionが見つかりませんでした。'
    default_code = 'option-not-found'


class OpNotPermission(APIException):
    status_code = 400
    default_detail = '権限がありません。'
    default_code = 'OriginalPoint-not-permission'


class TransactionNotFound(APIException):
    status_code = 400
    default_detail = 'transactionが見つかりませんでした。'
    default_code = 'Transaction-not-found'


class UnexpectedError(APIException):
    status_code = 400
    default_detail = '予期せぬエラーが発生しました'
    default_code = 'UnexpectedError'


# ユーザーが管理しているOPリスト
class UserManagementOpList(generics.ListAPIView):
    serializer_class = UserManagementOpListSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        return OpManagement.objects.filter(user=user, is_active=True)


# ユーザーが管理しているOPの詳細
class OpDetail(generics.ListAPIView):
    serializer_class = OriginalPointListSerializer

    def get_queryset(self):
        # op_nameパラメーターを変数op_nameに格納
        op_name = self.request.query_params.get("op_name")
        # リクエストしてきたuserの情報を変数userに格納
        user = self.request.user
        try:
            # OPからop_nameに合致したものを変数opに格納
            op = OriginalPoint.objects.get(name=op_name)
            # ユーザーが持っているOpManagementのuser・op・is_activeが合致した場合
            OpManagement.objects.get(user=user, op=op, is_active=True)
        # OPが見つからない場合
        except OriginalPoint.DoesNotExist:
            raise OriginalPointNotFound
        # OpManagementが合致しない場合
        except OpManagement.DoesNotExist:
            raise OpNotPermission
        return OriginalPoint.objects.filter(name=op_name)


class OriginalPointList(generics.ListAPIView):
    serializer_class = OriginalPointListSerializer
    queryset = OriginalPoint.objects.all()


# OPのトランザクションリスト
class MgTransactionList(generics.ListAPIView):
    serializer_class = TransactionSerializer
    filterset_fields = ['use_time', 'point', 'status', 'use_usage']
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['use_time', 'point', 'status', 'use_usage']
    pagination_class = TransactionListPagination

    def get_queryset(self):
        # op_nameパラメーターを変数op_nameに格納
        op_name = self.request.query_params.get("op_name")
        # リクエストしてきたuserの情報を変数userに格納
        user = self.request.user
        try:
            # OPからop_nameに合致したものを変数opに格納
            op = OriginalPoint.objects.get(name=op_name)
            # ユーザーが持っているOpManagementのuser・op・is_activeが合致した場合
            OpManagement.objects.get(user=user, op=op, is_active=True)
        # OPが見つからない場合
        except OriginalPoint.DoesNotExist:
            raise OriginalPointNotFound
        # OpManagementが合致しない場合
        except OpManagement.DoesNotExist:
            raise OpNotPermission
        # opのトランザクションを新順で取得
        return Transaction.objects.filter(op=op).order_by("-use_time")


class MgOpUserList(generics.ListAPIView):
    serializer_class = UserListSerializer
    pagination_class = UserListSerializerPagination

    def get_queryset(self):
        op_name = self.request.query_params.get("op_name")
        option = self.request.query_params.get("option")
        user = self.request.user
        try:
            op = OriginalPoint.objects.get(name=op_name)
            OpManagement.objects.get(user=user, op=op, is_active=True)
        except OriginalPoint.DoesNotExist:
            raise OriginalPointNotFound
        except OpManagement.DoesNotExist:
            raise OpNotPermission
        if option == "inviting_application_list":
            return UserAccount.objects.filter(opentryuser__op=op, opentryuser__is_active=False).order_by("name")
        elif option == "registration_user":
            return UserAccount.objects.filter(opentryuser__op=op, opentryuser__is_active=True).order_by("name")
        elif option == "wallet_registration_user":
            return UserAccount.objects.filter(wallet__op=op).order_by("name")
        else:
            raise OptionNotFound

        # OPのトランザクション検索


class MgTransactionSearch(generics.ListAPIView):
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # パラメーターでidを取得
    filterset_fields = ['id']
    pagination_class = TransactionListPagination

    def get_queryset(self):
        op_name = self.request.query_params.get("op_name")
        user = self.request.user
        try:
            op = OriginalPoint.objects.get(name=op_name)
            OpManagement.objects.get(user=user, op=op, is_active=True)
        except OriginalPoint.DoesNotExist:
            raise OriginalPointNotFound
        except OpManagement.DoesNotExist:
            raise OpNotPermission
        return Transaction.objects.filter(op=op).order_by("-use_time")


# OPのトランザクション詳細
@api_view(["GET"])
def t_detail(request):
    transaction_id = request.query_params.get("t_id")
    op_name = request.query_params.get("op_name")
    user = request.user
    try:
        op = OriginalPoint.objects.get(name=op_name)
        OpManagement.objects.get(user=user, op=op, is_active=True)
        transaction = Transaction.objects.get(id=transaction_id)
    except OriginalPoint.DoesNotExist:
        raise OriginalPointNotFound
    except OpManagement.DoesNotExist:
        raise OpNotPermission
    except Transaction.DoesNotExist:
        raise TransactionNotFound
    except ValidationError:
        raise TransactionNotFound
    if request.method == 'GET':
        context = {
            "id": transaction.id,
            "op_name": transaction.op.name,
            "op_id": transaction.op.id,
            "usage": transaction.use_usage,
            "time": transaction.use_time,
            "point": transaction.point,
            "trading_time": transaction.trading_time,
            "status": transaction.status,
        }
        if transaction.wallet is None:
            context["wallet"] = transaction.wallet
        else:
            context["wallet"] = transaction.wallet.id
        res = {"detail": context}
        return Response(res, status=status.HTTP_200_OK)


# OPのトランザクション作成
@api_view(["POST"])
def t_create(request):
    try:
        op_name = request.query_params.get("op_name")
        user = request.user
        use_usage = int(request.query_params.get("use_usage"))
        point = int(request.query_params.get("point"))
        op = OriginalPoint.objects.get(name=op_name)
        OpManagement.objects.get(user=user, op=op, is_active=True)
    except OriginalPoint.DoesNotExist:
        raise OriginalPointNotFound
    except OpManagement.DoesNotExist:
        raise OpNotPermission
    except Transaction.DoesNotExist:
        raise TransactionNotFound
    except ValidationError:
        raise TransactionNotFound
    except ValueError:
        raise UnexpectedError
    if use_usage == 0:
        usage_count = 1
        status_count = 2
    elif use_usage == 1:
        usage_count = 2
        status_count = 3
    else:
        raise UnexpectedError
    if 0 < point <= 99999999:
        if use_usage == 1:
            op.total_issuing_number += point
            op.save()
        transaction = Transaction.objects.create(op=op, use_usage=usage_count, status=status_count, point=point)
        transaction.save()
        t_id = transaction.id
        context = {"t_id": t_id}
        return Response({"detail": context}, status=status.HTTP_201_CREATED)
    else:
        raise UnexpectedError


# OPの設定
@api_view(["GET", "POST"])
def op_setting(request):
    op_name = request.query_params.get("op_name")
    user = request.user
    try:
        op = OriginalPoint.objects.get(name=op_name)
        OpManagement.objects.get(user=user, op=op, is_active=True)
    except OriginalPoint.DoesNotExist:
        raise OriginalPointNotFound
    except OpManagement.DoesNotExist:
        raise OpNotPermission
    if request.method == 'GET':
        context = {
            "detailed_name": op.detailed_name,
            "introduction": op.introduction,
            "cost": op.cost,
            "publishing": op.publishing
        }
        return Response(context, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data
        detailed_name = data["detailed_name"]
        introduction = data["introduction"]
        cost = data["cost"]
        publishing = data["publishing"]
        op.detailed_name = detailed_name
        op.introduction = introduction
        op.cost = cost
        op.publishing = publishing
        op.save()
        return Response({"detail": "設定成功しました。"}, status=status.HTTP_200_OK)


# OPの作成
@api_view(["GET", "POST"])
def op_create(request):
    user = request.user
    if request.method == 'GET':
        op_name = request.query_params.get("c_op_name")
        if op_name is None:
            return Response({"detail": "パラメーターが見つかりませんでした"}, status=status.HTTP_404_NOT_FOUND)
        try:
            OriginalPoint.objects.get(name=op_name)
        except OriginalPoint.DoesNotExist:
            return Response({"detail": "利用可能"}, status=status.HTTP_200_OK)
        return Response({"detail": "利用不可"}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        name = data["op_name"]
        detailed_name = data["detailed_name"]
        introduction = data["introduction"]
        cost = data["cost"]
        publishing = data["publishing"]
        try:
            op = OriginalPoint.objects.create(name=name, cost=cost, detailed_name=detailed_name,
                                              introduction=introduction,
                                              publishing=publishing)
        except IntegrityError:
            return Response({"detail": "その名前は既に使われています"}, status=status.HTTP_400_BAD_REQUEST)
        OpManagement.objects.create(user=user, op=op, is_active=True, permission_level=1)
        context = {"op_name": op.name}
        return Response({"detail": context}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
# GET(読み取り)未認証でもアクセス可能とする
@permission_classes((IsAuthenticatedOrReadOnly,))
def invite(request):
    user = request.user
    try:
        invite_id = request.query_params.get("invite_id")
        invitation = OpInvitation.objects.get(id=invite_id)
        if not invitation.is_active:
            res = {"result": "NO", "detail": "存在しないか利用できない招待リンクです。"}
            return Response(res)
        if invitation.time_limit != 0:
            elapsed_time = timezone.now() - invitation.use_time
            if elapsed_time.seconds >= invitation.time_limit:
                res = {"result": "NO", "detail": "利用期限切れの招待リンクです"}
                return Response(res)
        if invitation.use_limit_c != 0:
            if invitation.using_c >= invitation.use_limit_c:
                res = {"result": "NO", "detail": "利用期限切れの招待リンクです"}
                return Response(res)
        if not user.is_anonymous:
            try:
                OpEntryUser.objects.get(user=user, op=invitation.op)
                res = {"result": "NO", "detail": "参加しているか申請済みです。"}
                return Response(res)
            except OpEntryUser.DoesNotExist:
                var = None
    except OpInvitation.DoesNotExist:
        res = {"result": "NO", "detail": "存在しないか利用できない招待リンクです。"}
        return Response(res)
    except ValidationError:
        res = {"result": "NO", "detail": "存在しないか利用できない招待リンクです。"}
        return Response(res)

    if request.method == 'GET':
        context = {
            "id": invitation.id,
            "op_name": invitation.op.name,
        }
        res = {"result": "OK", "detail": context}
        return Response(res, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        op_entry = OpEntryUser.objects.create(op=invitation.op, user=user)
        op_entry.save()
        invitation.using_c += 1
        invitation.save()
        return Response({"result": "OK", "detail": "参加申請を送りました管理者のアクションをお待ちください。"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def inviteAction(request):
    op_name = request.query_params.get("op_name")
    action = request.query_params.get("action")
    user = request.user
    target_user_id = int(request.query_params.get("user_id"))
    try:
        target_user = UserAccount.objects.get(id=target_user_id)
        op = OriginalPoint.objects.get(name=op_name)
        OpManagement.objects.get(user=user, op=op, is_active=True)
        invite_user = OpEntryUser.objects.get(user=target_user, is_active=False, op=op)
    except OriginalPoint.DoesNotExist:
        raise OriginalPointNotFound
    except OpManagement.DoesNotExist:
        raise OpNotPermission
    except OpEntryUser.DoesNotExist:
        raise UnexpectedError
    except UserAccount.DoesNotExist:
        raise UnexpectedError
    if action == "approval":
        invite_user.is_active = True
        invite_user.save()
        try:
            Wallet.objects.get(user=target_user)
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=target_user, op=op)
            wallet.save()
            op.user_count += 1
            op.save()
            return Response({"result": "OK", "detail": "申請を承認しウォレットを発行しました。"}, status=status.HTTP_201_CREATED)
        return Response({"result": "OK", "detail": "申請を承認しました。"}, status=status.HTTP_201_CREATED)
    elif action == "rejection":
        invite_user.delete()
        return Response({"result": "OK", "detail": "申請を却下しました"}, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def inviteOptionSetting(request):
    op_name = request.query_params.get("op_name")
    user = request.user
    try:
        op = OriginalPoint.objects.get(name=op_name)
        OpManagement.objects.get(user=user, op=op, is_active=True)
    except OriginalPoint.DoesNotExist:
        raise OriginalPointNotFound
    except OpManagement.DoesNotExist:
        raise OpNotPermission
    except OpEntryUser.DoesNotExist:
        raise UnexpectedError
    except OpInvitation.DoesNotExist:
        return Response({"detail": "招待URLを作成してください"}, status=status.HTTP_200_OK)
    if request.method == 'GET':
        try:
            invitation = OpInvitation.objects.get(op=op)
        except OpInvitation.DoesNotExist:
            return Response({"detail": "招待URLを作成してください"}, status=status.HTTP_200_OK)
        context = {
            "id": invitation.id,
            "use_time": invitation.use_time,
            "time_limit": invitation.time_limit,
            "use_limit_count": invitation.use_limit_c,
            "using_count": invitation.using_c,
        }
        res = {"detail": context}
        return Response(res, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data
        time_limit = data["time_limit"]
        use_limit_count = data["use_limit_count"]
        try:
            invitation = OpInvitation.objects.get(op=op)
            invitation.delete()
            invitation = OpInvitation.objects.create(op=op, time_limit=time_limit, use_limit_c=use_limit_count,
                                                     is_active=True)
        except OpInvitation.DoesNotExist:
            invitation = OpInvitation.objects.create(op=op, time_limit=time_limit, use_limit_c=use_limit_count,
                                                     is_active=True)
        context = {
            "id": invitation.id,
            "use_time": invitation.use_time,
            "time_limit": invitation.time_limit,
            "use_limit_count": invitation.use_limit_c,
            "using_count": invitation.using_c,
        }
        return Response({"detail": context}, status=status.HTTP_201_CREATED)
