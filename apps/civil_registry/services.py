"""
Civil Registry business logic — birth, death, and marriage certificates.

Constitutional mandate: Chapter 4 (Bill of Rights, Art. 26-45) guarantees the right
to legal identity, family rights, and access to civil documentation.
"""
from django.db import transaction
from core.utils import generate_application_reference
from .models import BirthCertificate, DeathCertificate, MarriageCertificate


def _finalise(instance):
    instance.status = 'submitted'
    instance.save(update_fields=['status'])
    return instance


def submit_birth_certificate(*, user, child_name, date_of_birth, place_of_birth,
                              gender='male', father_name='', mother_name='',
                              county_of_birth='', **kwargs):
    ref = generate_application_reference('BTH')
    cert = BirthCertificate.objects.create(
        user=user, reference=ref,
        child_name=child_name, date_of_birth=date_of_birth,
        place_of_birth=place_of_birth, gender=gender,
        father_name=father_name, mother_name=mother_name,
        county_of_birth=county_of_birth,
        status='draft',
    )
    return _finalise(cert)


def submit_death_certificate(*, user, deceased_name, date_of_death, place_of_death,
                              cause_of_death='', gender='male', age_at_death=None,
                              next_of_kin='', informant_name='', **kwargs):
    ref = generate_application_reference('DTH')
    cert = DeathCertificate.objects.create(
        user=user, reference=ref,
        deceased_name=deceased_name, date_of_death=date_of_death,
        place_of_death=place_of_death, cause_of_death=cause_of_death,
        gender=gender, age_at_death=age_at_death,
        next_of_kin=next_of_kin, informant_name=informant_name,
        status='draft',
    )
    return _finalise(cert)


def submit_marriage_certificate(*, user, spouse1_name, spouse2_name, marriage_date,
                                 marriage_place='', marriage_type='civil',
                                 officiant_name='', **kwargs):
    ref = generate_application_reference('MRG')
    cert = MarriageCertificate.objects.create(
        user=user, reference=ref,
        spouse1_name=spouse1_name, spouse2_name=spouse2_name,
        marriage_date=marriage_date, marriage_place=marriage_place,
        marriage_type=marriage_type, officiant_name=officiant_name,
        status='draft',
    )
    return _finalise(cert)


def get_user_certificates(user, cert_type=None):
    """Return all certificates for a user, optionally filtered by type."""
    results = []
    if not cert_type or cert_type == 'birth':
        results.extend(BirthCertificate.objects.filter(user=user).order_by('-created_at'))
    if not cert_type or cert_type == 'death':
        results.extend(DeathCertificate.objects.filter(user=user).order_by('-created_at'))
    if not cert_type or cert_type == 'marriage':
        results.extend(MarriageCertificate.objects.filter(user=user).order_by('-created_at'))
    return sorted(results, key=lambda x: x.created_at, reverse=True)
