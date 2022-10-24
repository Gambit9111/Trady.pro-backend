from rest_framework import serializers
from .models import Trading_System, Symbol, Account, Transaction

class Trading_SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trading_System
        fields = ('id', 'name', 'description', 'image', 'created_at')

class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ('id', 'label')

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'label', 'balance', 'created_at')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'account', 'transaction_type', 'amount', 'created_at')