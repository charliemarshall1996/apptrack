
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
import pytest

from accounts.models import CustomUser


@pytest.fixture
def get_custom_user():
    return {'email': "8LH0L@example.com",
            'email_verified': True,
            'last_verification_email_sent': timezone.now() - timedelta(days=1),
            'first_name': "John", 'last_name': "Doe",
            'is_active': True,
            'is_staff': False,
            'date_joined': timezone.now() - timedelta(days=1)}


@pytest.fixture
def get_profile(get_custom_user):
    return {'user': CustomUser(**get_custom_user), 'email_comms_opt_in': True,
            'birth_date': timezone.now() - timedelta(days=1)}


@pytest.fixture
@pytest.mark.django_db
def create_users(get_custom_user):
    """Fixture to create users for testing."""
    get_custom_user['password'] = "securepassword"
    UserModel = get_user_model()

    UserModel.objects.filter(**get_custom_user).delete()

    # Verified user
    verified_user = UserModel.objects.create_user(**get_custom_user)
    verified_user.save()

    # Unverified user
    get_custom_user['email'] = "unverified@example.com"
    get_custom_user['email_verified'] = False
    unverified_user = UserModel.objects.create_user(**get_custom_user)
    unverified_user.save()

    yield {"verified_user": verified_user, "unverified_user": unverified_user}

    # Clean up after the test
    verified_user.delete()
    unverified_user.delete()
