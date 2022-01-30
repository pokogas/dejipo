from django.urls import path
from . import views

app_name = 'transaction'

urlpatterns = [
    path('user-transaction-list/', views.UserTransactionList.as_view(), name='user-transaction-list'),
    path('transaction-each-wallet-list/', views.TransactionEachWalletList.as_view(), name='transaction-each-wallet-list'),
    path('', views.detail, name='detail'),
]
