from rest_framework.routers import DefaultRouter
from ..views.api import PaymentTransactionViewSet, InvoiceViewSet, WalletViewSet, BankAccountViewSet

router = DefaultRouter()
router.register(r'transactions', PaymentTransactionViewSet, basename='payment')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'wallet', WalletViewSet, basename='wallet')
router.register(r'bank-accounts', BankAccountViewSet, basename='bankaccount')

urlpatterns = router.urls
