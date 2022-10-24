from django.urls import path

from .views import AccountListCreateView, AccountDetailView, TransactionListCreateView, TransactionDetailView, SymbolListCreateView, SymbolDetailView, Trading_SystemListCreateView, Trading_SystemDetailView

app_name = 'accounts'

urlpatterns = [
    path('', AccountListCreateView.as_view(), name='account-list-create'),
    path('<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('symbols/', SymbolListCreateView.as_view(), name='symbol-list-create'),
    path('symbols/<int:pk>/', SymbolDetailView.as_view(), name='symbol-detail'),
    path('trading-systems/', Trading_SystemListCreateView.as_view(), name='trading-system-list-create'),
    path('trading-systems/<int:pk>/', Trading_SystemDetailView.as_view(), name='trading-system-detail'),

]