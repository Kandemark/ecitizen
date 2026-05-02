"""
Tax services — tax returns, assessments, and compliance certificates.

Constitutional mandate: Chapter 11 (Public Finance, Art. 201-206) — principles of
public finance, equitable taxation, and fiscal responsibility.
"""
from decimal import Decimal
from core.utils import generate_application_reference
from .models import TaxReturn, TaxAssessment, ComplianceCertificate


def submit_tax_return(*, user, tax_type, tax_period, period_start=None,
                        period_end=None, amount=Decimal('0'), kra_pin='', **kwargs):
    ref = generate_application_reference('TAX')
    ret = TaxReturn.objects.create(
        user=user, reference=ref,
        tax_type=tax_type, tax_period=tax_period,
        period_start=period_start, period_end=period_end,
        amount=amount, kra_pin=kra_pin, status='draft',
    )
    ret.status = 'submitted'
    ret.save(update_fields=['status'])
    return ret


def submit_tax_assessment(*, user, assessment_year, tax_type,
                            total_income=Decimal('0'), taxable_income=Decimal('0'),
                            total_assessed=Decimal('0'), tax_paid=Decimal('0'),
                            kra_pin='', **kwargs):
    ref = generate_application_reference('ASM')
    assessment = TaxAssessment.objects.create(
        user=user, reference=ref,
        assessment_year=assessment_year, tax_type=tax_type,
        total_income=total_income, taxable_income=taxable_income,
        total_assessed=total_assessed, tax_paid=tax_paid,
        balance_due=total_assessed - tax_paid,
        kra_pin=kra_pin, status='draft',
    )
    assessment.status = 'submitted'
    assessment.save(update_fields=['status'])
    return assessment


def submit_compliance_certificate(*, user, certificate_type, kra_pin='', **kwargs):
    ref = generate_application_reference('CMP')
    cert = ComplianceCertificate.objects.create(
        user=user, reference=ref,
        certificate_type=certificate_type, kra_pin=kra_pin,
        status='draft',
    )
    cert.status = 'submitted'
    cert.save(update_fields=['status'])
    return cert


def get_user_records(user):
    return {
        'returns': TaxReturn.objects.filter(user=user).order_by('-created_at'),
        'assessments': TaxAssessment.objects.filter(user=user).order_by('-created_at'),
        'certificates': ComplianceCertificate.objects.filter(user=user).order_by('-created_at'),
    }
