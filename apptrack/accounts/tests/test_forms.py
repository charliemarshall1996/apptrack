import pytest
from datetime import date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from accounts.forms import (
    UserRegistrationForm,
    ProfileRegistrationForm,
    UserUpdateForm,
    ProfileUpdateForm,
    UserLoginForm,
    ResendVerificationEmailForm,
    PasswordResetForm,
)
from accounts.models import Profile


@pytest.mark.django_db
def test_user_registration_form_valid(user_registration_form_data):
    form = UserRegistrationForm(data=user_registration_form_data)
    assert form.is_valid()
    user = form.save()
    assert user.email == user_registration_form_data['email']
    user.save()
    user.delete()


@pytest.mark.django_db
def test_user_registration_form_invalid_email(user_registration_form_data):
    user_registration_form_data['email'] = "invalid-email"
    form = UserRegistrationForm(data=user_registration_form_data)
    assert not form.is_valid()
    assert 'Enter a valid email address.' in form.errors["email"]


@pytest.mark.django_db
def test_profile_registration_form_valid(create_users):
    form_data = {
        "birth_date": "2000-01-01",
        "email_comms_opt_in": True,
    }
    form = ProfileRegistrationForm(data=form_data)
    assert form.is_valid()

    # Save the profile and associate it with the verified user
    profile = form.save()  # Save but don't commit yet
    # Associate with verified user
    profile.user = create_users['verified_user']
    profile.save()  # Now save the profile

    # Assertions
    assert profile.birth_date == date(2000, 1, 1)
    assert profile.email_comms_opt_in is True

    # Cleanup
    profile.delete()


@pytest.mark.django_db
def test_profile_registration_form_invalid_birth_date():
    form_data = {
        "birth_date": "invalid-date",
        "email_comms_opt_in": True,
    }
    form = ProfileRegistrationForm(data=form_data)
    assert not form.is_valid()
    assert "Enter a valid date." in form.errors["birth_date"]


@pytest.mark.django_db
def test_user_update_form_valid():
    form_data = {
        "email": "updated@example.com",
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
    }
    form = UserUpdateForm(data=form_data)
    assert form.is_valid()
    user = form.save()
    assert user.email == "updated@example.com"
    assert user.first_name == "UpdatedFirstName"
    assert user.last_name == "UpdatedLastName"

    user.save()
    user.delete()


@pytest.mark.django_db
def test_profile_update_form_valid(create_users):
    profile, _ = Profile.objects.get_or_create(
        user=create_users['verified_user'])
    profile.birth_date = date(2000, 1, 1)
    profile.email_comms_opt_in = False
    profile.save()
    form_data = {
        "birth_date": "1995-05-15",
        "email_comms_opt_in": True,
    }
    form = ProfileUpdateForm(instance=profile, data=form_data)
    assert form.is_valid()
    updated_profile = form.save()
    assert updated_profile.birth_date == date(1995, 5, 15)
    assert updated_profile.email_comms_opt_in is True
    profile.delete()
    updated_profile.save()
    updated_profile.delete()


def test_user_login_form_valid():
    form_data = {
        "email": "test@example.com",
        "password": "StrongPassword123",
    }
    form = UserLoginForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data["email"] == "test@example.com"


def test_user_login_form_missing_fields():
    form_data = {
        "email": "",
        "password": "",
    }
    form = UserLoginForm(data=form_data)
    assert not form.is_valid()
    assert "email" in form.errors
    assert "password" in form.errors


def test_resend_verification_email_form_valid():
    form_data = {"email": "test@example.com"}
    form = ResendVerificationEmailForm(data=form_data)
    assert form.is_valid()


def test_resend_verification_email_form_invalid_email():
    form_data = {"email": "invalid-email"}
    form = ResendVerificationEmailForm(data=form_data)
    assert not form.is_valid()
    assert "Enter a valid email address." in form.errors["email"]


def test_password_reset_form_valid():
    form_data = {"email": "test@example.com"}
    form = PasswordResetForm(data=form_data)
    assert form.is_valid()


def test_password_reset_form_invalid_email():
    form_data = {"email": "invalid-email"}
    form = PasswordResetForm(data=form_data)
    assert not form.is_valid()
    assert "Enter a valid email address." in form.errors["email"]
