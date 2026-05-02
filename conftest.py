"""
Shared pytest fixtures for the eCitizen test suite.
"""
import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    """Create a regular citizen user."""
    return User.objects.create_user(
        username='citizen_test',
        email='citizen@example.com',
        password='testpass123',
    )


@pytest.fixture
def staff_user(db):
    """Create a staff user for authorities/workflow tests."""
    return User.objects.create_user(
        username='staff_test',
        email='staff@example.com',
        password='testpass123',
        is_staff=True,
    )


@pytest.fixture
def admin_user(db):
    """Create a superuser."""
    return User.objects.create_superuser(
        username='admin_test',
        email='admin@example.com',
        password='testpass123',
    )


@pytest.fixture
def client():
    """Django test client."""
    from django.test import Client
    return Client()


@pytest.fixture
def authenticated_client(client, user):
    """Client logged in as a regular user."""
    client.force_login(user)
    return client


@pytest.fixture
def staff_client(client, staff_user):
    """Client logged in as a staff user."""
    client.force_login(staff_user)
    return client
