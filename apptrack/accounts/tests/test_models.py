
import pytest

from accounts.models import *


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


@pytest.mark.django_db
def test_profile(get_profile):

    model = Profile(**get_profile)
    assert model.user == get_profile['user']
    assert model.email_comms_opt_in == get_profile['email_comms_opt_in']
    assert model.birth_date == get_profile['birth_date']
