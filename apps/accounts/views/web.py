from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

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
@ensure_csrf_cookie
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
    user_county = None
    county_code = '047'  # default to Nairobi

    # Determine user's county: profile > session geolocation > default
    profile = getattr(user, 'profile', None)
    if profile and profile.county:
        county_code = profile.county.code
        user_county = profile.county
    else:
        session_code = request.session.get('detected_county')
        if session_code:
            county_code = session_code

    try:
        from apps.integration.services.weather import fetch_county_weather
        weather = fetch_county_weather(county_code)
    except Exception:
        pass

    # Fetch county services if we have a county, grouped by function
    county_services_grouped = []
    county_info = None
    try:
        from apps.counties.models import County
        county = County.objects.filter(code=county_code, is_active=True).first()
        if county:
            county_info = {
                'code': county.code,
                'name': county.name,
                'capital': county.capital,
            }
            svcs = list(county.services.filter(
                is_active=True, constitutional_function__isnull=False
            ).select_related('constitutional_function').order_by(
                'constitutional_function__order', 'name'
            ))
            # Group by constitutional function, limit to 3 groups, 4 services each
            by_func = {}
            for svc in svcs:
                key = svc.constitutional_function.name
                if key not in by_func:
                    by_func[key] = []
                by_func[key].append(svc)
            for name, svc_list in list(by_func.items())[:3]:
                county_services_grouped.append({
                    'name': name,
                    'services': svc_list[:4],
                })
    except Exception:
        pass

    context = {
        'user': user,
        'profile': profile,
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
        'county_info': county_info,
        'county_services_grouped': county_services_grouped,
        'county_code': county_code,
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

    # Build account info summary
    account_info = {
        'username': user.username,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'is_verified': profile.is_verified if profile else False,
        'role': profile.get_role_display() if profile else 'Citizen',
    }

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'update_avatar' and profile and request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
            profile.save()
            messages.success(request, 'Profile photo updated.')
            return redirect('profile')

        if action == 'update_profile':
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()

            if profile:
                profile.phone = request.POST.get('phone', profile.phone)
                profile.id_number = request.POST.get('id_number', profile.id_number)
                profile.gender = request.POST.get('gender', profile.gender)
                profile.date_of_birth = request.POST.get('date_of_birth') or profile.date_of_birth
                profile.postal_address = request.POST.get('postal_address', profile.postal_address)
                profile.city = request.POST.get('city', profile.city)

                county_id = request.POST.get('county')
                if county_id:
                    try:
                        from apps.counties.models import County
                        profile.county = County.objects.get(id=county_id)
                    except Exception:
                        pass

                profile.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

        messages.error(request, 'Invalid action.')
        return redirect('profile')

    counties = []
    try:
        from apps.counties.models import County
        counties = list(County.objects.filter(is_active=True).values('id', 'name').order_by('name'))
    except Exception:
        pass

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'account_info': account_info,
        'counties': counties,
    })


@login_required
def account_security(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'change_password':
            current = request.POST.get('current_password', '')
            new = request.POST.get('new_password', '')
            confirm = request.POST.get('confirm_password', '')
            if not user.check_password(current):
                messages.error(request, 'Current password is incorrect.')
            elif new != confirm:
                messages.error(request, 'New passwords do not match.')
            elif len(new) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
            elif current == new:
                messages.error(request, 'New password must be different from your current password.')
            else:
                user.set_password(new)
                user.save()
                from django.contrib.auth import login
                login(request, user)
                messages.success(request, 'Password updated successfully.')
                return redirect('account_security')

        elif action == 'set_transaction_pin':
            pin = request.POST.get('transaction_pin', '')
            confirm_pin = request.POST.get('confirm_transaction_pin', '')
            current_password = request.POST.get('current_password_for_pin', '')
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif len(pin) != 4 or not pin.isdigit():
                messages.error(request, 'Transaction PIN must be exactly 4 digits.')
            elif pin != confirm_pin:
                messages.error(request, 'PINs do not match.')
            elif profile:
                from django.contrib.auth.hashers import make_password
                profile.transaction_pin = make_password(pin)
                profile.save()
                messages.success(request, 'Transaction PIN set successfully.')
                return redirect('account_security')
            else:
                messages.error(request, 'Profile not found.')

    # Build security score
    security_checks = []
    score = 0
    max_score = 6

    # Password check
    has_strong_pw = len(user.password) > 30  # hashed passwords are long
    if has_strong_pw:
        score += 1
        security_checks.append({'label': 'Password set', 'passed': True, 'detail': 'Your account is password-protected.'})
    else:
        security_checks.append({'label': 'Password set', 'passed': False, 'detail': 'Set a strong password for your account.'})

    # Email verified (proxy check)
    if user.email:
        score += 1
        security_checks.append({'label': 'Email address', 'passed': True, 'detail': 'Recovery email is configured.'})
    else:
        security_checks.append({'label': 'Email address', 'passed': False, 'detail': 'Add an email for account recovery.'})

    # Phone set
    if profile and profile.phone:
        score += 1
        security_checks.append({'label': 'Phone number', 'passed': True, 'detail': 'SMS notifications and recovery enabled.'})
    else:
        security_checks.append({'label': 'Phone number', 'passed': False, 'detail': 'Add a phone number for SMS alerts and recovery.'})

    # ID verified
    if profile and profile.is_verified:
        score += 1
        security_checks.append({'label': 'Identity verified', 'passed': True, 'detail': 'Your identity has been verified.'})
    else:
        security_checks.append({'label': 'Identity verified', 'passed': False, 'detail': 'Complete identity verification for full access.'})

    # Transaction PIN
    if profile and profile.transaction_pin:
        score += 1
        security_checks.append({'label': 'Transaction PIN', 'passed': True, 'detail': 'Payment confirmation PIN is set.'})
    else:
        security_checks.append({'label': 'Transaction PIN', 'passed': False, 'detail': 'Set a PIN to authorize payments and sensitive actions.'})

    # 2FA placeholder
    security_checks.append({'label': 'Two-factor authentication', 'passed': False, 'detail': 'Enable 2FA for additional account protection.'})

    security_score = {
        'score': score,
        'max': max_score,
        'percentage': int((score / max_score) * 100),
        'level': 'Strong' if score >= 5 else ('Good' if score >= 3 else 'Needs Attention'),
        'level_color': '#0b6e4f' if score >= 5 else ('#e6a817' if score >= 3 else '#d93025'),
    }

    # Recent audit entries for this user
    recent_activity = []
    try:
        from .models import AuditEntry
        recent_activity = AuditEntry.objects.filter(
            user=user
        ).order_by('-created_at')[:8]
    except Exception:
        pass

    # Session info
    session_info = {
        'ip': request.META.get('REMOTE_ADDR', 'Unknown'),
        'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown')[:120],
        'session_start': request.session.get('_session_init', 'Unknown'),
        'is_secure': request.is_secure(),
    }

    return render(request, 'accounts/account_security.html', {
        'profile': profile,
        'security_score': security_score,
        'security_checks': security_checks,
        'recent_activity': recent_activity,
        'session_info': session_info,
    })


@login_required
def privacy_settings(request):
    profile = getattr(request.user, 'profile', None)
    prefs = profile.preferences if profile else {}

    if request.method == 'POST':
        profile_visible = request.POST.get('profile_visible') == 'on'
        data_sharing = request.POST.get('data_sharing') == 'on'
        analytics_opt = request.POST.get('analytics_opt') == 'on'
        marketing_opt = request.POST.get('marketing_opt') == 'on'
        activity_log = request.POST.get('activity_log') == 'on'

        if profile:
            profile.preferences = {
                'profile_visible': profile_visible,
                'data_sharing': data_sharing,
                'analytics_opt': analytics_opt,
                'marketing_opt': marketing_opt,
                'activity_log': activity_log,
            }
            profile.save()

        messages.success(request, 'Privacy settings updated.')
        return redirect('privacy_settings')

    return render(request, 'accounts/privacy_settings.html', {
        'preferences': prefs,
        'profile': profile,
    })


@login_required
def user_roles_access(request):
    return render(request, 'accounts/user_roles_access_levels.html')


def about_view(request):
    stats = {}
    try:
        from apps.services.models import Service
        stats['service_count'] = Service.objects.filter(is_active=True).count()
    except Exception:
        stats['service_count'] = 0

    try:
        from apps.counties.models import County
        stats['county_count'] = County.objects.filter(is_active=True).count()
    except Exception:
        stats['county_count'] = 47

    try:
        from apps.ministries.models import Ministry
        stats['ministry_count'] = Ministry.objects.filter(is_active=True).count()
    except Exception:
        stats['ministry_count'] = 0

    try:
        from apps.services.models import ConstitutionalFunction
        stats['county_functions_count'] = ConstitutionalFunction.objects.filter(is_active=True).count()
    except Exception:
        stats['county_functions_count'] = 14

    return render(request, 'accounts/about.html', {'stats': stats})


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
