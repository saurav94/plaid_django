from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Transaction, Account, Item

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['item', 'account_id','available_balance', 'current_balace', 'name', 'account_type', 'account_subtype']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['account', 'transaction_id' ,'amount', 'date', 'name', 'payment_channel']
