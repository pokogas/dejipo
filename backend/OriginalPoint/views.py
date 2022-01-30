from rest_framework import generics, status
from rest_framework.response import Response
from .models import Wallet, OriginalPoint
from .serializers import WalletCreateSerializer


# ウォレット作成
class WalletCreate(generics.CreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletCreateSerializer

    def create(self, request, *args, **kwargs):
        # op_idパラメーターを変数op_idに格納
        op_id = self.request.query_params.get("op_id")
        # リクエストしてきたuserの情報を変数userに格納
        user = self.request.user
        # Walletモデルにuser,op_idを入れて.saveでWalletを作成
        Wallet(user=user, op_id=op_id).save()
        # OriginalPointの利用者数に+1追加
        originalpoint = OriginalPoint.objects.get(id=op_id)
        originalpoint.user_count += 1
        originalpoint.save()
        return Response({"detail": "ウォレットを作成しました。"}, status=status.HTTP_201_CREATED)
