from django.contrib import admin
from .models import PaymentTransaction, Invoice, Receipt, Wallet, WalletTransaction, BankAccount


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'amount', 'currency', 'status', 'mpesa_receipt', 'created_at']
    list_filter = ['status', 'currency']
    search_fields = ['reference', 'mpesa_receipt', 'user__username']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'total_amount', 'is_paid', 'due_date']
    list_filter = ['is_paid']
    search_fields = ['reference', 'user__username']


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'payment', 'issued_by', 'created_at']
    search_fields = ['receipt_number']


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['wallet_id', 'user', 'balance', 'currency', 'is_active', 'created_at']
    list_filter = ['is_active', 'currency']
    search_fields = ['wallet_id', 'user__username']


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'wallet', 'transaction_type', 'amount', 'created_at']
    list_filter = ['transaction_type']
    search_fields = ['reference', 'wallet__wallet_id']


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'bank_name', 'is_verified', 'is_primary']
    list_filter = ['is_verified', 'is_primary']
    search_fields = ['account_number', 'user__username', 'bank_name']
