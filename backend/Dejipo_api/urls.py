from django.urls import path
from . import views

app_name = 'dejipo'

urlpatterns = [
    path('user-wallet-list/', views.WalletList.as_view(), name='user_wallet_list'),
    path('user-wallet-detail/', views.WalletDetail.as_view(), name='user-wallet-detail'),
    path('original-point-list/', views.OriginalPointList.as_view(), name='original-point-list'),
]
