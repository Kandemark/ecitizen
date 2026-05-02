"""
Immigration services — passport, visa, and work permit applications.

Constitutional mandate: Chapter 3 (National Executive, Art. 132) — foreign affairs
and immigration control. Also Chapter 4 (Bill of Rights, Art. 39) — freedom of movement.
"""
from core.utils import generate_application_reference
from .models import PassportApplication, VisaApplication, WorkPermit


def submit_passport(*, user, passport_type='ordinary', **kwargs):
    ref = generate_application_reference('PSP')
    app = PassportApplication.objects.create(
        user=user, reference=ref,
        passport_type=passport_type,
        status='draft',
    )
    app.status = 'submitted'
    app.save(update_fields=['status'])
    return app


def submit_visa(*, user, visa_type, **kwargs):
    ref = generate_application_reference('VSA')
    app = VisaApplication.objects.create(
        user=user, reference=ref,
        visa_type=visa_type,
        status='draft',
    )
    app.status = 'submitted'
    app.save(update_fields=['status'])
    return app


def submit_work_permit(*, user, permit_class, employer='', **kwargs):
    ref = generate_application_reference('WKP')
    permit = WorkPermit.objects.create(
        user=user, reference=ref,
        permit_class=permit_class, employer=employer,
        status='draft',
    )
    permit.status = 'submitted'
    permit.save(update_fields=['status'])
    return permit


def get_user_applications(user):
    passports = PassportApplication.objects.filter(user=user).order_by('-created_at')
    visas = VisaApplication.objects.filter(user=user).order_by('-created_at')
    permits = WorkPermit.objects.filter(user=user).order_by('-created_at')
    return {
        'passports': passports,
        'visas': visas,
        'work_permits': permits,
    }
