
from datetime import timedelta
import random

from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
import pytest

from accounts.models import Profile
from core.choices import ReminderUnitChoices
from jobs.choices import (
    CurrencyChoices,
    CountryChoices,
    JobFunctionChoices,
    LocationPolicyChoices,
    WorkContractChoices,
    PayRateChoices,
    StatusChoices,
    SourceChoices,
)
from jobs.models import Job, Board, Column

UserModel = get_user_model()

fake = Faker()

SOURCES = [source[0] for source in SourceChoices.choices()]
JOB_FUNCTIONS = [job[0] for job in JobFunctionChoices.choices()]
LOCATION_POLICIES = [loc[0] for loc in LocationPolicyChoices.choices()]
WORK_CONTRACT = [work[0] for work in WorkContractChoices.choices()]
PAY_RATES = [pay[0] for pay in PayRateChoices.choices()]
CURRENCIES = [currency[0] for currency in CurrencyChoices.choices()]
STATUSES = [status[0] for status in StatusChoices.choices()]
COUNTRIES = [country[0] for country in CountryChoices.choices()]


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
        'company': fake.company(),
        'town': fake.city(),
        'region': fake.state(),
        "country": random.choice(COUNTRIES),
    }


@pytest.fixture()
def jobs_data():
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
        'company': fake.company(),
        'town': fake.city(),
        'country': random.choice(COUNTRIES),
        'region': fake.state(),
    }


@pytest.fixture()
def job_data_factory():
    def factory(updated_days_previous=None):
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
            'company': fake.company(),
            'town': fake.city(),
            'country': random.choice(COUNTRIES),
            'region': fake.state(),
            'updated': timezone.now() - timedelta(days=updated_days_previous)
            if updated_days_previous else None,
        }
    return factory


@pytest.fixture()
def job_form_factory(jobs_form_data):
    def factory(user=None):
        return Job(user=user, **jobs_form_data)
    return factory


@pytest.fixture
def job_factory(job_data_factory):

    def factory(user, updated_days_previous=None):
        data = job_data_factory(updated_days_previous)
        return Job(user=user, **data)
    return factory


@pytest.fixture
def board_data_factory(custom_user_factory):
    def factory(user=None, password=None, email_verified=True, name=None, no_name=False):
        if not user:
            user = custom_user_factory(
                password=password, email_verified=email_verified)

        if no_name:
            return {'user': user}
        return {'user': user, 'name': name or fake.job()}
    return factory


@pytest.fixture()
def board_factory(board_data_factory):
    def factory(user=None, password=None, email_verified=True, name=None, no_name=False):
        data = board_data_factory(
            user, password, email_verified, name, no_name)
        return Board(**data)
    return factory


@pytest.fixture()
def column_data_factory():
    def factory(name=None, position=None, board=None):
        if not name:
            name = random.choice(STATUSES)
            position = StatusChoices.get_status_column_position(name)
        elif not position:
            position = StatusChoices.get_status_column_position(name)
        if not board:
            return {'name': name or random.choice(STATUSES), 'position': position or random.randint(1, 7)}
        else:
            return {'name': name or random.choice(STATUSES), 'position': position or random.randint(1, 7), 'board': board}
    return factory


@pytest.fixture()
def column_factory(column_data_factory):
    def factory(name=None, position=None, board=None):
        data = column_data_factory(name, position, board)
        return Column(**data)
    return factory


@pytest.fixture()
def task_data_factory():
    def factory(name=None, is_completed=False):
        return {'name': name or ' '.join(fake.words(3)), 'is_completed': is_completed}
    return factory


@pytest.fixture()
def reminder_data_factory(custom_user_factory):
    def factory(user=None, password=None, read=False, emailed=False):
        if not user:
            user = custom_user_factory(
                password=password)
        return {'user': user,
                'unit': random.choice(ReminderUnitChoices.choices()),
                'offset': random.randint(1, 10),
                'emailed': emailed,
                'read': read
                }
    return factory
