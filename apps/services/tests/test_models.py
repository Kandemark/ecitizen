"""
Tests for Service, ServiceCategory, RequiredDocument, and EligibilityRule models.
"""
import pytest
from apps.services.models import Service, ServiceCategory, RequiredDocument, EligibilityRule


@pytest.mark.django_db
class TestServiceModel:
    def test_create_service(self):
        cat = ServiceCategory.objects.create(name='Test Category')
        service = Service.objects.create(
            name='Test Service',
            slug='test-service',
            category=cat,
            is_active=True,
        )
        assert str(service) == 'Test Service'
        assert service.slug == 'test-service'

    def test_service_defaults(self):
        cat = ServiceCategory.objects.create(name='Cat')
        service = Service.objects.create(name='Svc', slug='svc', category=cat)
        assert service.is_active is True  # Default is True for new services
        assert service.slug == 'svc'


@pytest.mark.django_db
class TestRequiredDocument:
    def test_create_document(self):
        doc = RequiredDocument.objects.create(
            name='Test Document',
            document_type='test_doc',
            description='A test document',
            is_mandatory=True,
        )
        assert str(doc) == 'Test Document'
        assert doc.is_mandatory is True


@pytest.mark.django_db
class TestEligibilityRule:
    def test_create_rule(self):
        rule = EligibilityRule.objects.create(
            name='Test Rule',
            description='Must be 18+',
            min_age=18,
        )
        assert rule.min_age == 18
