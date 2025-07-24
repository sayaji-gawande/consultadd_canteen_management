from django.urls import path
from .views import AddMoneyView, PurchaseItemView, PassbookView, AllTransactionsAdminView, AdminAddMoneyView

urlpatterns = [
    path('add-money/', AddMoneyView.as_view(), name='add-money'),
    path('purchase/', PurchaseItemView.as_view(), name='purchase-item'),
    path('passbook/', PassbookView.as_view(), name='employee-passbook'),
    path('all-transactions/', AllTransactionsAdminView.as_view(), name='all-transactions-admin'),
    path('admin-add-money/', AdminAddMoneyView.as_view(), name='admin-add-money'),
]
