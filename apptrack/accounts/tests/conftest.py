
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
import pytest

from accounts.models import CustomUser, Profile

UserModel = get_user_model()


@pytest.fixture
def user_registration_form_data(email=None, password1=None, password2=None, first_name=None, last_name=None):
    return {
        "email": "8LH0L@example.com",
        "password1": "secur3password.",
        "password2": "secur3password.",
        "first_name": "John",
        "last_name": "Doe",
    }


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
    get_custom_user['password'] = "securepassword"
    user = UserModel.objects.create_user(**get_custom_user)
    user.save()
    return {'user': user, 'email_comms_opt_in': True,
            'birth_date': timezone.now() - timedelta(days=1)}


@pytest.fixture
@pytest.mark.django_db
def create_users(get_custom_user):
    """Fixture to create users for testing."""
    get_custom_user['password'] = "securepassword"

    # Clean up any existing users with the same email before creating new ones
    UserModel.objects.filter(**get_custom_user).delete()

    # Create a verified user
    verified_user = UserModel.objects.create_user(**get_custom_user)
    verified_user.save()

    # Create an unverified user
    get_custom_user['email'] = "unverified@example.com"
    get_custom_user['email_verified'] = False
    unverified_user = UserModel.objects.create_user(**get_custom_user)
    unverified_user.save()

    yield {"verified_user": verified_user, "unverified_user": unverified_user}

    # Cleanup: Ensure profiles are deleted if they exist
    for user in [verified_user, unverified_user]:
        if hasattr(user, 'profile') and user.profile:
            user.profile.save()
            user.profile.delete()  # Only delete if profile exists
        user.delete()  # Delete the user object itself
