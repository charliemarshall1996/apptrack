
from datetime import timedelta
from typing import Dict

from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
import pytest

from accounts.models import Profile

UserModel = get_user_model()

fake = Faker()


@pytest.fixture
def user_registration_form_data():
    password = fake.password()
    yield {
        "email": fake.email(),
        "password1": password,
        "password2": password,
        "first_name": fake.file_name(),
        "last_name": fake.last_name(),
    }


@pytest.fixture
def custom_user_data_factory():
    def factory(password=None, email_verified=True):
        return {
            'email': fake.email(),
            'email_verified': email_verified,
            'last_verification_email_sent': timezone.now() - timedelta(days=1),
            'first_name': fake.file_name(),
            'last_name': fake.file_name(),
            'is_active': True,
            'is_staff': False,
            'password': password or fake.password(),
            'date_joined': timezone.now() - timedelta(days=1),
        }
    return factory


@pytest.fixture
def custom_user_factory(custom_user_data_factory):

    def factory(password=None, email_verified=True):
        data = custom_user_data_factory(password, email_verified)
        return UserModel.objects.create_user(**data)
    return factory


@pytest.fixture
def profile_data_factory():
    def factory(user):
        return {'user': user,
                'email_comms_opt_in': True,
                'birth_date': timezone.now() - timedelta(days=1)}
    return factory


@pytest.fixture
@pytest.mark.django_db
def create_users(custom_user_data_factory) -> Dict[str, UserModel]:
    """Fixture to create users for testing."""
    data = custom_user_data_factory()
    users = UserModel.objects.filter(email=data['email'])
    for user in users:
        if hasattr(user, "profile"):
            user.profile.delete()
        user.delete()

    data['password'] = "securepassword"

    # Create a verified user
    verified_user = UserModel.objects.create_user(**data)
    verified_user.save()

    # Create an unverified user
    data['email_verified'] = False
    unverified_user = UserModel.objects.create_user(**data)
    unverified_user.save()

    print(f"VERIFIED EMAIL: {verified_user.email}")
    print(f"UNVERIFIED EMAIL: {unverified_user.email}")
    yield {"verified_user": verified_user, "unverified_user": unverified_user}


@pytest.fixture
def profile_factory(custom_user_factory, profile_data_factory):
    def factory(password=None, email_verified=True):
        user = custom_user_factory(
            password=password, email_verified=email_verified)
        data = profile_data_factory(user)
        return Profile(**data)
    return factory
