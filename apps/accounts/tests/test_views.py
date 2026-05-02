"""
Tests for accounts web views — dashboard, services, payments.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboardView:
    def test_redirects_anonymous(self, client):
        resp = client.get(reverse('dashboard'))
        assert resp.status_code == 302
        assert '/login/' in resp.url

    def test_renders_for_authenticated(self, authenticated_client):
        resp = authenticated_client.get(reverse('dashboard'))
        assert resp.status_code == 200
        assert b'e-Citizen' in resp.content


@pytest.mark.django_db
class TestServicesView:
    def test_loads_for_anonymous(self, client):
        resp = client.get(reverse('services_list'))
        assert resp.status_code == 200

    def test_renders_for_authenticated(self, authenticated_client):
        resp = authenticated_client.get(reverse('services_list'))
        assert resp.status_code == 200


@pytest.mark.django_db
class TestPaymentsView:
    def test_redirects_anonymous(self, client):
        resp = client.get(reverse('payments_list'))
        assert resp.status_code == 302

    def test_renders_for_authenticated(self, authenticated_client):
        resp = authenticated_client.get(reverse('payments_list'))
        assert resp.status_code == 200


@pytest.mark.django_db
class TestLoginView:
    def test_login_page_loads(self, client):
        resp = client.get(reverse('login'))
        assert resp.status_code == 200
        assert b'login' in resp.content.lower()

    def test_login_authenticates(self, client, user):
        resp = client.post(reverse('login'), {
            'username': 'citizen_test',
            'password': 'testpass123',
        })
        assert resp.status_code == 302
        assert resp.url == reverse('dashboard')
