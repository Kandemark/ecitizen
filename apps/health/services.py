"""
Health services — health records, NHIF registration, medical certificates.

Constitutional mandate: Chapter 4 (Bill of Rights, Art. 43) — right to the highest
attainable standard of health, including reproductive health care.
"""
from core.utils import generate_application_reference
from .models import HealthRecord, NHIFRegistration, MedicalCertificate


def submit_health_record(*, user, facility_name, record_type, visit_date=None,
                           diagnosis='', prescription='', attending_practitioner='',
                           notes='', **kwargs):
    ref = generate_application_reference('HLT')
    rec = HealthRecord.objects.create(
        user=user, reference=ref,
        facility_name=facility_name, record_type=record_type,
        visit_date=visit_date, diagnosis=diagnosis,
        prescription=prescription, attending_practitioner=attending_practitioner,
        notes=notes, status='draft',
    )
    rec.status = 'submitted'
    rec.save(update_fields=['status'])
    return rec


def submit_nhif_registration(*, user, employer_name='', monthly_contribution=0,
                               dependants=0, **kwargs):
    ref = generate_application_reference('NHF')
    reg = NHIFRegistration.objects.create(
        user=user, reference=ref,
        employer_name=employer_name, monthly_contribution=monthly_contribution,
        dependants=dependants, status='draft',
    )
    reg.status = 'submitted'
    reg.save(update_fields=['status'])
    return reg


def submit_medical_certificate(*, user, certificate_type, issuing_facility,
                                 issuing_practitioner='', issued_date=None,
                                 expiry_date=None, findings='', **kwargs):
    ref = generate_application_reference('MED')
    cert = MedicalCertificate.objects.create(
        user=user, reference=ref,
        certificate_type=certificate_type, issuing_facility=issuing_facility,
        issuing_practitioner=issuing_practitioner, issued_date=issued_date,
        expiry_date=expiry_date, findings=findings, status='draft',
    )
    cert.status = 'submitted'
    cert.save(update_fields=['status'])
    return cert


def get_user_records(user):
    return {
        'records': HealthRecord.objects.filter(user=user).order_by('-created_at'),
        'nhif': NHIFRegistration.objects.filter(user=user).order_by('-created_at'),
        'certificates': MedicalCertificate.objects.filter(user=user).order_by('-created_at'),
    }
