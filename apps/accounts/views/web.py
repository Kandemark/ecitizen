from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from ..models import Profile


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Welcome back!')
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    applications = []
    notifications = []
    wallet = None
    recent_payments = []
    indicators = {}
    exchange_rates = {}
    upcoming_appointments = []
    recent_documents = []

    if hasattr(user, 'profile'):
        try:
            from apps.applications.models import Application
            applications = Application.objects.filter(user=user).order_by('-created_at')[:5]
        except Exception:
            pass

    try:
        from apps.notifications.models import Notification
        notifications = Notification.objects.filter(
            user=user, is_read=False,
        ).order_by('-created_at')[:10]
    except Exception:
        pass

    try:
        wallet = user.wallet
        recent_payments = wallet.transactions.order_by('-created_at')[:5]
    except Exception:
        pass

    try:
        from core.kenya_data import get_economic_indicators, get_exchange_rates
        indicators = get_economic_indicators()
        exchange_rates = get_exchange_rates()
    except Exception:
        pass

    try:
        from apps.appointments.models import Appointment
        upcoming_appointments = Appointment.objects.filter(
            user=user, status__in=['scheduled', 'confirmed']
        ).select_related('service', 'time_slot').order_by('time_slot__date', 'time_slot__start_time')[:5]
    except Exception:
        pass

    try:
        from apps.documents.models import Document
        recent_documents = Document.objects.filter(
            user=user
        ).order_by('-created_at')[:5]
    except Exception:
        pass

    quick_links = []
    try:
        from apps.services.cache import get_popular_services
        quick_links = get_popular_services(6)
    except Exception:
        try:
            from apps.services.models import Service
            quick_links = list(Service.objects.filter(
                is_popular=True, is_active=True
            ).values('name', 'slug', 'icon')[:6])
        except Exception:
            pass

    # Fallback if no popular services exist
    if not quick_links:
        quick_links = [
            {'name': 'Browse All Services', 'slug': '', 'icon': 'Grid', 'url': '/services/browse/'},
        ]

    news_articles = []
    try:
        from apps.news.models import NewsArticle
        news_articles = NewsArticle.objects.select_related('source').order_by('-published_at')[:6]
    except Exception:
        pass

    weather = None
    try:
        from apps.integration.services.weather import fetch_county_weather
        # Try Nairobi (047) as default; in future use user's county
        weather = fetch_county_weather('047')
    except Exception:
        pass

    context = {
        'user': user,
        'profile': getattr(user, 'profile', None),
        'recent_applications': applications,
        'notifications': notifications,
        'quick_links': quick_links,
        'wallet': wallet,
        'recent_payments': recent_payments,
        'indicators': indicators,
        'exchange_rates': exchange_rates,
        'upcoming_appointments': upcoming_appointments,
        'recent_documents': recent_documents,
        'news_articles': news_articles,
        'weather': weather,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def latest_notifications(request):
    notifications = []
    try:
        from apps.notifications.models import Notification
        notifications = Notification.objects.filter(
            user=request.user, is_read=False,
        ).order_by('-created_at')[:10]
    except Exception:
        pass
    return render(request, 'accounts/includes/notification_feed.html', {
        'notifications': notifications,
    })


@login_required
def profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        if profile:
            profile.phone = request.POST.get('phone', profile.phone)
            profile.id_number = request.POST.get('id_number', profile.id_number)
            profile.gender = request.POST.get('gender', profile.gender)
            profile.postal_address = request.POST.get('postal_address', profile.postal_address)
            profile.save()
        messages.success(request, 'Profile updated.')
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def account_security(request):
    if request.method == 'POST':
        user = request.user
        current = request.POST.get('current_password', '')
        new = request.POST.get('new_password', '')
        confirm = request.POST.get('confirm_password', '')
        if not user.check_password(current):
            messages.error(request, 'Current password is incorrect.')
        elif new != confirm:
            messages.error(request, 'New passwords do not match.')
        elif len(new) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            user.set_password(new)
            user.save()
            login(request, user)
            messages.success(request, 'Password updated successfully.')
            return redirect('account_security')
    return render(request, 'accounts/account_security.html')


@login_required
def privacy_settings(request):
    return render(request, 'accounts/privacy_settings.html')


@login_required
def user_roles_access(request):
    return render(request, 'accounts/user_roles_access_levels.html')


def about_view(request):
    return render(request, 'accounts/about.html')


def contact_view(request):
    from ..forms import ContactForm
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent. We will get back to you soon.')
            return redirect('contact')
    return render(request, 'accounts/contact.html', {'form': form})


@login_required
def applications_list(request):
    applications = []
    try:
        from apps.applications.models import Application as AppModel
        applications = AppModel.objects.filter(user=request.user).order_by('-created_at')
    except Exception:
        pass
    return render(request, 'accounts/applications.html', {'applications': applications})


@login_required
def payments_list(request):
    payments = []
    invoices = []
    wallet = None

    try:
        from apps.payments.models import PaymentTransaction, Invoice
        payments_qs = PaymentTransaction.objects.filter(
            user=request.user
        ).select_related('application__service')

        # Filter by status
        status = request.GET.get('status', '')
        if status:
            payments_qs = payments_qs.filter(status=status)

        # Filter by date range
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', '')
        if date_from:
            payments_qs = payments_qs.filter(created_at__date__gte=date_from)
        if date_to:
            payments_qs = payments_qs.filter(created_at__date__lte=date_to)

        payments = payments_qs.order_by('-created_at')[:50]
        invoices = Invoice.objects.filter(
            user=request.user
        ).select_related('service').order_by('-created_at')[:20]
    except Exception:
        pass

    try:
        wallet = request.user.wallet
    except Exception:
        pass

    context = {
        'payments': payments,
        'invoices': invoices,
        'wallet': wallet,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'accounts/includes/payment_list.html', context)

    return render(request, 'accounts/payments.html', context)


def services_list(request):
    services = []
    categories = []
    popular = []
    try:
        from apps.services.models import Service, ServiceCategory
        services = Service.objects.filter(is_active=True)
        categories = ServiceCategory.objects.filter(is_active=True)
        popular = Service.objects.filter(is_popular=True, is_active=True)[:6]
    except Exception:
        pass
    return render(request, 'accounts/services.html', {
        'services': services,
        'categories': categories,
        'popular_services': popular,
    })
