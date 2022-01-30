from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('user-management-op-list/', views.UserManagementOpList.as_view(), name='user_management_op_list'),
    path('management-op-create/', views.op_create, name='user_management_op_create'),
    path('management-transaction-list/', views.MgTransactionList.as_view(), name='management-transaction-list'),
    path('management-transaction-search/', views.MgTransactionSearch.as_view(), name='management-transaction-search'),
    path('management-transaction-detail/', views.t_detail, name='management-transaction-detail'),
    path('management-transaction-create/', views.t_create, name='management-transaction-create'),
    path('management-op-setting/', views.op_setting, name='management-op-setting'),
    path('management-op-invite/', views.invite, name='management-op-invite'),
    path('management-op-invite-action/', views.inviteAction, name='management-op-invite-action'),
    path('management-op-invite-option-setting/', views.inviteOptionSetting, name='management-op-invite-option-setting'),
    path('management-op-user-list/', views.MgOpUserList.as_view(), name='management-op-user-list'),
    path('op-detail/', views.OpDetail.as_view(), name='op-detail'),
]
