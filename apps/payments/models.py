from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.constants import PAYMENT_STATUSES


class PaymentTransaction(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    application = models.ForeignKey(
        'applications.Application', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    status = models.CharField(max_length=15, choices=PAYMENT_STATUSES, default='pending')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    mpesa_receipt = models.CharField(max_length=30, blank=True)
    mpesa_phone = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reference} — {self.amount} {self.currency} ({self.status})'


class Invoice(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    service = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    reference = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'Invoice {self.reference} — {self.total_amount} KES'


class Receipt(TimestampMixin):
    payment = models.OneToOneField(PaymentTransaction, on_delete=models.CASCADE, related_name='receipt')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    receipt_number = models.CharField(max_length=30, unique=True)
    issued_by = models.CharField(max_length=100, default='e-Citizen')

    def __str__(self):
        return self.receipt_number


class Wallet(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default='KES')
    is_active = models.BooleanField(default=True)
    wallet_id = models.CharField(max_length=30, unique=True, db_index=True)

    def __str__(self):
        return f'{self.wallet_id} — {self.balance} {self.currency}'


class WalletTransaction(TimestampMixin):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('transfer', 'Transfer'),
    ]
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_before = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    description = models.TextField(blank=True)
    payment_transaction = models.ForeignKey(
        PaymentTransaction, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='wallet_transactions'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reference} — {self.transaction_type} {self.amount}'


class BankAccount(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_accounts')
    bank_name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=10)
    branch = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=30)
    account_name = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f'{self.bank_name} — {self.account_number}'
