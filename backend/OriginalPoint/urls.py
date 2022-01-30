from django.urls import path
from . import views

app_name = 'op'

urlpatterns = [
    path('wallet-create/', views.WalletCreate.as_view(), name='wallet-create'),
]
