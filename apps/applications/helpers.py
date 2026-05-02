"""
Helper to bridge ministry-specific model submissions with the generic
Application model and workflow engine.

Every ministry web view should call `create_workflow_application` after
creating a ministry-specific record (BirthCertificate, PassportApplication, etc.).
This ensures the application appears in the authorities review queue and
workflow engine.
"""
import logging
from django.db import transaction
from django.utils import timezone
from apps.applications.models import Application

logger = logging.getLogger(__name__)

# Map each ministry model's goal to a Service slug in the catalog.
# When a BirthCertificate is submitted, the matching Service is looked up.
MODEL_TO_SERVICE_SLUG = {
    # civil_registry
    'BirthCertificate': 'birth-certificate-application',
    'DeathCertificate': 'death-certificate-application',
    'MarriageCertificate': 'civil-marriage-registration',
    # immigration
    'PassportApplication': 'passport-application',
    'VisaApplication': 'visa-application',
    'WorkPermit': 'work-permit-application',
    # transport
    'DrivingLicense': 'driving-license-application',
    'VehicleRegistration': 'vehicle-registration',
    'PSVLicense': 'road-service-license',
    'VehicleInspection': 'motor-vehicle-search',
    # land
    'TitleDeed': 'land-title-search',
    'LandSearch': 'land-title-search',
    'Transfer': 'property-transfer-registration',
    # health
    'HealthRecord': 'nhif-registration',
    'NHIFRegistration': 'nhif-registration',
    'MedicalCertificate': 'medical-practitioner-license',
    # taxes
    'TaxReturn': 'tax-compliance-certificate',
    'TaxAssessment': 'tax-compliance-certificate',
    'ComplianceCertificate': 'tax-compliance-certificate',
    # education
    'LoanApplication': 'university-admission',
    'SchoolRegistration': 'university-admission',
    'ExamResult': 'kcpe-kcse-results',
    # licenses
    'BusinessLicense': 'single-business-permit',
    'ProfessionalCertification': 'medical-practitioner-license',
    # judiciary
    'CourtCase': 'single-business-permit',
    'Filing': 'single-business-permit',
    'Fine': 'tax-compliance-certificate',
    # procurement
    'Bid': 'single-business-permit',
    # public_participation
    'Petition': 'single-business-permit',
}


def create_workflow_application(instance, user):
    """
    Given a ministry-specific model instance (e.g. BirthCertificate),
    find the matching Service, create a generic Application record,
    and trigger the workflow engine.

    Returns the Application or None.
    """
    model_name = type(instance).__name__
    slug = MODEL_TO_SERVICE_SLUG.get(model_name)
    if not slug:
        return None

    try:
        from apps.services.models import Service
        service = Service.objects.get(slug=slug)
    except Exception:
        logger.debug('No Service found for slug=%s (model=%s)', slug, model_name)
        return None

    try:
        with transaction.atomic():
            app = Application.objects.create(
                user=user,
                service=service,
                reference=instance.reference,
                status='submitted',
                submitted_at=timezone.now(),
                form_data=_extract_fields(instance),
            )
    except Exception as exc:
        logger.warning('Failed to create Application for %s: %s', model_name, exc)
        return None

    # Trigger workflow
    try:
        from apps.workflow.services import WorkflowEngine
        WorkflowEngine.on_application_submitted(app)
    except Exception as exc:
        logger.warning('Workflow trigger skipped for %s: %s', model_name, exc)

    return app


def _extract_fields(instance):
    """Pull relevant fields from a model instance into a flat dict."""
    skip = {'id', 'created_at', 'updated_at', 'is_deleted', 'deleted_at',
            'user', 'user_id', 'reference', 'status'}
    data = {}
    for field in instance._meta.get_fields():
        if field.name in skip or field.is_relation:
            continue
        try:
            val = getattr(instance, field.name)
            if val is not None:
                data[field.name] = str(val) if not isinstance(val, (str, int, float, bool)) else val
        except Exception:
            pass
    return data
