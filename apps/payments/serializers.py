from rest_framework import serializers
from .models import PaymentTransaction, Invoice, Receipt, Wallet, WalletTransaction, BankAccount


class PaymentTransactionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PaymentTransaction
        fields = ['id', 'user', 'user_name', 'application', 'amount', 'currency', 'status', 'reference', 'mpesa_receipt', 'mpesa_phone', 'description', 'created_at']
        read_only_fields = ['reference', 'status', 'mpesa_receipt']

    def create(self, validated_data):
        from core.utils import generate_receipt_number
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_receipt_number()
        return super().create(validated_data)


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'user', 'service', 'amount', 'tax_amount', 'total_amount', 'description', 'due_date', 'is_paid', 'reference']
        read_only_fields = ['reference', 'is_paid']


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'payment', 'invoice', 'receipt_number', 'issued_by', 'created_at']


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = ['id', 'wallet', 'transaction_type', 'amount', 'balance_before', 'balance_after', 'reference', 'description', 'payment_transaction', 'created_at']
        read_only_fields = ['reference', 'balance_before', 'balance_after']


class WalletSerializer(serializers.ModelSerializer):
    recent_transactions = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'user_name', 'wallet_id', 'balance', 'currency', 'is_active', 'recent_transactions', 'created_at']
        read_only_fields = ['balance', 'wallet_id']

    def get_recent_transactions(self, obj):
        recent = obj.transactions.all()[:5]
        return WalletTransactionSerializer(recent, many=True).data


class BankAccountSerializer(serializers.ModelSerializer):
    bank_name_display = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = ['id', 'user', 'bank_name', 'bank_code', 'bank_name_display', 'branch', 'account_number', 'account_name', 'is_primary', 'is_verified', 'created_at']
        read_only_fields = ['is_verified']

    def get_bank_name_display(self, obj):
        from core.constants import KENYAN_BANKS
        for code, name in KENYAN_BANKS:
            if code == obj.bank_code:
                return name
        return obj.bank_name
