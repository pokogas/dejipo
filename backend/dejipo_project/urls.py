from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/account/', include('Account.urls')),
    path('api/dejipo/', include('Dejipo_api.urls')),
    path('api/transaction/', include('Transaction.urls')),
    path('api/management/', include('Management.urls')),
    path('api/op/', include('OriginalPoint.urls')),
    path('admin/', admin.site.urls),
]
