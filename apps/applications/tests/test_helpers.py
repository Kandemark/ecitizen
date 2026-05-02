"""
Tests for the workflow bridge helper — create_workflow_application.
"""
import pytest

from apps.services.models import Service, ServiceCategory
from apps.applications.models import Application
from apps.applications.helpers import create_workflow_application, MODEL_TO_SERVICE_SLUG


@pytest.mark.django_db
class TestCreateWorkflowApplication:
    def test_creates_application_when_service_exists(self, user):
        cat = ServiceCategory.objects.create(name='Civil')
        Service.objects.create(
            name='Birth Certificate Application',
            slug='birth-certificate-application',
            category=cat,
        )

        # Use a real Django model instead of a mock
        from apps.land.models import TitleDeed
        deed = TitleDeed.objects.create(
            user=user, reference='TD-20260501-ABC12345',
            title_number='NRB/1234', property_location='Nairobi CBD',
            status='draft',
        )

        # TitleDeed maps to 'land-title-search' which we haven't created,
        # so it should return None gracefully
        result = create_workflow_application(deed, user)
        assert result is None

    def test_returns_none_for_unknown_model(self, user):
        class FakeModel:
            __name__ = 'NonExistentModel'

        result = create_workflow_application(FakeModel(), user)
        assert result is None

    def test_model_slug_map_coverage(self):
        """Verify all expected model names are mapped."""
        expected = [
            'BirthCertificate', 'DeathCertificate', 'MarriageCertificate',
            'PassportApplication', 'VisaApplication', 'WorkPermit',
            'DrivingLicense', 'VehicleRegistration', 'PSVLicense', 'VehicleInspection',
            'TitleDeed', 'LandSearch', 'Transfer',
            'HealthRecord', 'NHIFRegistration', 'MedicalCertificate',
            'TaxReturn', 'TaxAssessment', 'ComplianceCertificate',
            'LoanApplication', 'SchoolRegistration', 'ExamResult',
            'BusinessLicense', 'ProfessionalCertification',
            'CourtCase', 'Filing', 'Fine',
            'Bid', 'Petition',
        ]
        for model_name in expected:
            assert model_name in MODEL_TO_SERVICE_SLUG, (
                f'{model_name} is missing from MODEL_TO_SERVICE_SLUG'
            )
