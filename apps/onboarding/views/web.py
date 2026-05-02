from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import OnboardingProgress
from core.constants import COUNTIES, ID_TYPES, GENDER_CHOICES


def onboarding_wizard(request):
    """Public onboarding wizard — account creation happens in step 3."""

    # Redirect already-logged-in users who have completed onboarding
    if request.user.is_authenticated:
        progress, _ = OnboardingProgress.objects.get_or_create(user=request.user)
        if progress.is_complete:
            messages.info(request, 'You have already completed onboarding.')
            return redirect('dashboard')
        return _render_onboarding(request, progress)

    # Anonymous user — use session to store progress
    session = request.session
    if 'onboarding_step' not in session:
        session['onboarding_step'] = 1
        session['onboarding_data'] = {}
        session.save()

    step = session['onboarding_step']
    data = session.get('onboarding_data', {})

    if request.method == 'POST':
        step, data = _process_anonymous_step(request, step, data)
        if step == 0:
            return redirect('dashboard')
        session['onboarding_step'] = step
        session['onboarding_data'] = data
        session.save()

    context = {
        'step': step,
        'total_steps': 10,
        'step_title': _step_title(step),
    }
    if step == 5:  # Location step
        context['counties'] = COUNTIES
    return render(request, f'onboarding/step_{step}.html', context)


def _render_onboarding(request, progress):
    """Render onboarding for authenticated users."""
    step = progress.current_step
    context = {'step': step, 'total_steps': 10}

    if request.method == 'POST':
        step = _process_step(progress, request.POST)
        if step == 0:
            return redirect('dashboard')

    context['step'] = step
    context['step_title'] = _step_title(step)
    if step == 5:
        context['counties'] = COUNTIES
    return render(request, f'onboarding/step_{step}.html', context)


def _process_anonymous_step(request, step, data):
    """Process step data for unauthenticated users. Creates account at step 3."""

    if step == 1:  # Welcome
        data['language'] = request.POST.get('language', 'en')

    elif step == 2:  # ID Type
        data['id_type'] = request.POST.get('id_type', 'national_id')

    elif step == 3:  # Account & Personal Info — CREATE USER HERE
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')

        # Validate
        errors = []
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        if User.objects.filter(username=username).exists():
            errors.append('That username is already taken.')
        if not email:
            errors.append('Email is required.')
        if User.objects.filter(email=email).exists():
            errors.append('An account with that email already exists.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')

        if errors:
            messages.error(request, ' '.join(errors))
            return step, data  # stay on same step

        # Create user and log them in
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            password=password,
        )

        from apps.accounts.models import Profile
        Profile.objects.create(user=user)

        login(request, user)

        # Migrate session data to OnboardingProgress
        progress, _ = OnboardingProgress.objects.get_or_create(user=user)
        progress.data = {
            'language': data.get('language', 'en'),
            'id_type': data.get('id_type', 'national_id'),
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'date_of_birth': request.POST.get('date_of_birth', ''),
            'gender': request.POST.get('gender', ''),
        }
        progress.current_step = 4  # skip ahead past account creation
        progress.save()

        # Clear session onboarding data
        request.session.pop('onboarding_step', None)
        request.session.pop('onboarding_data', None)
        request.session.save()

        messages.success(request, f'Welcome, {user.first_name or username}! Let\'s complete your profile.')
        return progress.current_step, {}

    elif step == 4:  # Contact Info
        data.update({
            'phone': request.POST.get('phone', ''),
            'email_supplied': request.POST.get('email', ''),
            'postal_address': request.POST.get('postal_address', ''),
        })

    elif step == 5:  # Location
        data.update({
            'county_id': request.POST.get('county', ''),
            'sub_county_id': request.POST.get('sub_county', ''),
            'ward_id': request.POST.get('ward', ''),
        })

    elif step == 6:  # ID Verification
        data['id_number'] = request.POST.get('id_number', '')

    elif step == 7:  # Biometric placeholder
        pass

    elif step == 8:  # Transaction PIN
        pin = request.POST.get('transaction_pin', '')
        confirm_pin = request.POST.get('confirm_pin', '')
        if pin and pin == confirm_pin and len(pin) >= 4:
            import hashlib
            data['transaction_pin'] = hashlib.sha256(pin.encode()).hexdigest()
        else:
            messages.error(request, 'PIN must be at least 4 digits and must match.')

    elif step == 9:  # Preferences
        data['preferences'] = {
            'email_notifications': request.POST.get('email_notifications', 'on') == 'on',
            'sms_notifications': request.POST.get('sms_notifications', 'on') == 'on',
        }

    elif step == 10:  # Complete
        _finalize_anonymous_onboarding(request, data)
        return 0, {}

    step += 1
    if step > 10:
        step = 10
    return step, data


def _finalize_anonymous_onboarding(request, data):
    """Finalize onboarding for a user who created their account via onboarding."""
    user = request.user
    if not user.is_authenticated:
        return

    from apps.accounts.models import Profile
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.id_type = data.get('id_type', 'national_id')
    profile.id_number = data.get('id_number', '')
    profile.phone = data.get('phone', '')
    profile.gender = data.get('gender', '')
    if data.get('date_of_birth'):
        profile.date_of_birth = data['date_of_birth']
    if data.get('county_id'):
        profile.county_id = data['county_id']
    if data.get('sub_county_id'):
        profile.sub_county_id = data['sub_county_id']
    if data.get('ward_id'):
        profile.ward_id = data['ward_id']
    if data.get('village_id'):
        profile.village_id = data['village_id']
    profile.transaction_pin = data.get('transaction_pin', '')
    profile.is_verified = True
    profile.preferences = data.get('preferences', {})
    profile.save()

    from apps.payments.models import Wallet
    from core.utils import generate_tracking_id
    if not hasattr(user, 'wallet'):
        Wallet.objects.create(
            user=user,
            balance=0.00,
            wallet_id=generate_tracking_id('WLT'),
        )

    progress, _ = OnboardingProgress.objects.get_or_create(user=user)
    progress.is_complete = True
    progress.data = data
    progress.current_step = 10
    progress.save()
    messages.success(user, 'Onboarding complete! Welcome to e-Citizen.')


def _process_step(progress, data):
    """Process step data for authenticated users."""
    step = progress.current_step

    if step == 1:  # Welcome
        lang = data.get('language', 'en')
        progress.data['language'] = lang
    elif step == 2:  # ID Type
        progress.data['id_type'] = data.get('id_type', 'national_id')
    elif step == 3:  # Personal Info (for already-authenticated users)
        progress.data.update({
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'date_of_birth': data.get('date_of_birth', ''),
            'gender': data.get('gender', ''),
        })
    elif step == 4:  # Contact Info
        progress.data.update({
            'phone': data.get('phone', ''),
            'email': data.get('email', ''),
            'postal_address': data.get('postal_address', ''),
        })
    elif step == 5:  # Location
        progress.data.update({
            'county_id': data.get('county', ''),
            'sub_county_id': data.get('sub_county', ''),
            'ward_id': data.get('ward', ''),
            'village_id': data.get('village', ''),
        })
    elif step == 6:  # ID Verification
        progress.data['id_number'] = data.get('id_number', '')
    elif step == 7:  # Biometric
        pass
    elif step == 8:  # Transaction PIN
        pin = data.get('transaction_pin', '')
        confirm = data.get('confirm_pin', '')
        if pin and pin == confirm and len(pin) >= 4:
            import hashlib
            progress.data['transaction_pin'] = hashlib.sha256(pin.encode()).hexdigest()
    elif step == 9:  # Preferences
        progress.data['preferences'] = {
            'email_notifications': data.get('email_notifications', 'on') == 'on',
            'sms_notifications': data.get('sms_notifications', 'on') == 'on',
        }
    elif step == 10:  # Complete
        _finalize_onboarding(progress)
        return 0

    progress.advance_step()
    return progress.current_step


def _finalize_onboarding(progress):
    user = progress.user
    data = progress.data

    from apps.accounts.models import Profile
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.id_type = data.get('id_type', 'national_id')
    profile.id_number = data.get('id_number', '')
    profile.phone = data.get('phone', '')
    profile.gender = data.get('gender', '')
    if data.get('date_of_birth'):
        profile.date_of_birth = data['date_of_birth']
    if data.get('county_id'):
        profile.county_id = data['county_id']
    if data.get('sub_county_id'):
        profile.sub_county_id = data['sub_county_id']
    if data.get('ward_id'):
        profile.ward_id = data['ward_id']
    if data.get('village_id'):
        profile.village_id = data['village_id']
    profile.transaction_pin = data.get('transaction_pin', '')
    profile.is_verified = True
    profile.preferences = data.get('preferences', {})
    profile.save()

    from apps.payments.models import Wallet
    from core.utils import generate_tracking_id
    if not hasattr(user, 'wallet'):
        Wallet.objects.create(
            user=user,
            balance=0.00,
            wallet_id=generate_tracking_id('WLT'),
        )

    progress.is_complete = True
    progress.save()
    messages.success(progress.user, 'Onboarding complete! Welcome to e-Citizen.')


def _step_title(step):
    titles = {
        1: 'Welcome to e-Citizen',
        2: 'Select Your ID Type',
        3: 'Create Your Account',
        4: 'Contact Information',
        5: 'Your Location',
        6: 'ID Verification',
        7: 'Biometric Capture',
        8: 'Transaction PIN',
        9: 'Notification Preferences',
        10: 'All Done!',
    }
    return titles.get(step, '')
