
from datetime import timedelta
import random
from typing import Dict

from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
import pytest

from accounts.models import Profile
from jobs.models import Jobs, Boards, Columns

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
def profile_factory(custom_user_factory, profile_data_factory):
    def factory(password=None, email_verified=True):
        user = custom_user_factory(
            password=password, email_verified=email_verified)
        data = profile_data_factory(user)
        return Profile(**data)
    return factory


@pytest.fixture
def jobs_form_data():
    SOURCES = [source[0] for source in Jobs.SOURCE_CHOICES]
    JOB_FUNCTIONS = [job[0] for job in Jobs.JOB_FUNCTION_CHOICES]
    LOCATION_POLICIES = [loc[0] for loc in Jobs.LOCATION_POLICY_CHOICES]
    WORK_CONTRACT = [work[0] for work in Jobs.WORK_CONTRACT_CHOICES]
    PAY_RATES = [pay[0] for pay in Jobs.PAY_RATE_CHOICES]
    CURRENCIES = [currency[0] for currency in Jobs.PAY_CURRENCY_CHOICES]
    STATUSES = [status[0] for status in Jobs.STATUS_CHOICES]
    return {
        'url': fake.url(),
        'source': random.choice(SOURCES),
        'job_title': fake.job(),
        'job_function': random.choice(JOB_FUNCTIONS),
        'description': fake.text(),
        'location_policy': random.choice(LOCATION_POLICIES),
        'work_contract': random.choice(WORK_CONTRACT),
        'min_pay': random.randint(0, 10000),
        'max_pay': random.randint(10000, 100000),
        'pay_rate': random.choice(PAY_RATES),
        'currency': random.choice(CURRENCIES),
        'note': fake.text(),
        'status': random.choice(STATUSES),
    }


@pytest.fixture
def job_factory(jobs_form_data):
    def factory():
        return Jobs(**jobs_form_data)
    return factory


@pytest.fixture()
def board_factory(custom_user_factory):
    def factory(user=None, password=None, email_verified=True):
        if not user:
            user = custom_user_factory(
                password=password, email_verified=email_verified)
        return Boards(user=user)
    return factory


@pytest.fixture()
def column_data_factory():
    def factory(name=None, position=None, board=None):
        if not board:
            return {'name': name or fake.job(), 'position': position or random.randint(1, 9)}
        else:
            return {'name': name or fake.job(), 'position': position or random.randint(1, 9), 'board': board}
    return factory


@pytest.fixture()
def column_factory(column_data_factory):
    def factory(name=None, position=None, board=None):
        data = column_data_factory(name, position, board)
        return Columns(**data)
    return factory
