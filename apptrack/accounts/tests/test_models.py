
from datetime import timedelta
from django.utils import timezone
import pytest

from accounts.models import *


@pytest.fixture
def get_custom_user():
    return {'email': "8LH0L@example.com",
            'email_verified': True,
            'last_verification_email_sent': timezone.now() - timedelta(days=1),
            'first_name': "John", 'last_name': "Doe",
            'is_active': True,
            'is_staff': False,
            'date_joined': timezone.now() - timedelta(days=1)}


@pytest.mark.django_db
def test_custom_user(get_custom_user):
    model = CustomUser(**get_custom_user)
    assert model.email == get_custom_user['email']
    assert model.email_verified == get_custom_user['email_verified']
    assert model.last_verification_email_sent == get_custom_user['last_verification_email_sent']
    assert model.first_name == get_custom_user['first_name']
    assert model.last_name == get_custom_user['last_name']
    assert model.is_active == get_custom_user['is_active']
    assert model.is_staff == get_custom_user['is_staff']
    assert model.date_joined == get_custom_user['date_joined']
