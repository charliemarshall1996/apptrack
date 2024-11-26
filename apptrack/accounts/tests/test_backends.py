
from django.contrib.auth import authenticate
import pytest


@pytest.mark.django_db
def test_authenticate_verified_user(create_users):
    """Test that an email-verified user can authenticate."""
    user = authenticate(email="8LH0L@example.com",
                        password="securepassword")
    assert user is not None
    assert user.email == "8LH0L@example.com"


@pytest.mark.django_db
def test_authenticate_unverified_user(create_users):
    """Test that an unverified user cannot authenticate."""
    user = authenticate(email="unverified@example.com",
                        password="securepassword")
    assert user is None


@pytest.mark.django_db
def test_authenticate_non_existent_user(create_users):
    """Test that a non-existent user cannot authenticate."""
    user = authenticate(email="nonexistent@example.com",
                        password="securepassword")
    assert user is None


@pytest.mark.django_db
def test_authenticate_invalid_password(create_users):
    """Test that an invalid password cannot authenticate."""
    user = authenticate(email="8LH0L@example.com", password="wrongpassword")
    assert user is None
