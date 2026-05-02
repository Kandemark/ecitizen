from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.mixins import OwnerFilterMixin
from core.utils import generate_tracking_id
from ..models import PaymentTransaction, Invoice, Receipt, Wallet, WalletTransaction, BankAccount
from ..serializers import (
    PaymentTransactionSerializer, InvoiceSerializer, ReceiptSerializer,
    WalletSerializer, WalletTransactionSerializer, BankAccountSerializer,
)


class PaymentTransactionViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = PaymentTransaction.objects.all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        payment = serializer.save()
        try:
            wallet = payment.user.wallet
            balance_before = wallet.balance
            wallet.balance -= payment.amount
            wallet.save()
            WalletTransaction.objects.create(
                wallet=wallet,
                transaction_type='payment',
                amount=-payment.amount,
                balance_before=balance_before,
                balance_after=wallet.balance,
                reference=generate_tracking_id('WTR'),
                payment_transaction=payment,
                description=payment.description or 'Service payment',
            )
        except Wallet.DoesNotExist:
            pass

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        payment = self.get_object()
        mpesa_receipt = request.data.get('mpesa_receipt', '')
        if mpesa_receipt:
            payment.status = 'completed'
            payment.mpesa_receipt = mpesa_receipt
            payment.save()
            Receipt.objects.create(
                payment=payment,
                receipt_number=mpesa_receipt,
            )
            return Response({'status': 'completed'})
        return Response({'detail': 'Receipt number required.'}, status=400)


class InvoiceViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Wallet.objects.all()
        return Wallet.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def top_up(self, request):
        amount = request.data.get('amount')
        try:
            amount = float(amount)
            if amount <= 0:
                return Response({'detail': 'Amount must be positive.'}, status=400)
        except (TypeError, ValueError):
            return Response({'detail': 'Invalid amount.'}, status=400)

        wallet, _ = Wallet.objects.get_or_create(
            user=request.user,
            defaults={'wallet_id': generate_tracking_id('WLT')},
        )
        balance_before = wallet.balance
        wallet.balance += amount
        wallet.save()
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type='deposit',
            amount=amount,
            balance_before=balance_before,
            balance_after=wallet.balance,
            reference=generate_tracking_id('WTR'),
            description=f'Top-up via {request.data.get("method", "M-Pesa")}',
        )
        return Response(WalletSerializer(wallet).data)


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return BankAccount.objects.all()
        return BankAccount.objects.filter(user=self.request.user)
