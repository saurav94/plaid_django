from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='plaid-home'),
    
    path('get_access_token/', views.AccessTokenCreate.as_view()),
    path('get_public_token/', views.PublicTokenCreate.as_view()),
    path('get_transactions/', views.TransactionsGet.as_view()),
    path('get_transactions_from_db/', views.TransactionsGetDB.as_view()),
    path('get_account_balance/', views.AccountBalance.as_view()),
    path('get_account_balance_from_db/', views.AccountBalanceDB.as_view()),
    
    path('webhook_test/', views.WebhookTest.as_view()),
    path('webhook_transactions/', views.WebhookTransactions.as_view())
]