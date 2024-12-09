
from datetime import timedelta
import random

from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
import pytest

from accounts.models import Profile
from core.choices import ReminderUnitChoices
from jobs.choices import (
    StatusChoices,
    SourceChoices
)
from jobs.models import Job, Board, Column
from blog.models import BlogPost
from interview.models import Interview

UserModel = get_user_model()

fake = Faker()

SOURCES = [source[0] for source in SourceChoices.choices()]
STATUSES = [status[0] for status in StatusChoices.choices()]


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
        # 'job_function': random.choice(JOB_FUNCTIONS),
        'description': fake.text(),
        # 'location_policy': '',
        # 'work_contract': '',
        'min_pay': random.randint(0, 10000),
        'max_pay': random.randint(10000, 100000),
        # 'pay_rate': random.choice(PAY_RATES),
        # 'currency': '',
        'note': fake.text(),
        'status': random.choice(STATUSES),
        'company': fake.company(),
        'city': fake.city(),
        'region': fake.state(),
        # "country": '',
    }


@pytest.fixture()
def jobs_data():
    return {
        'url': fake.url(),
        'source': random.choice(SOURCES),
        'job_title': fake.job(),
        # 'job_function': random.choice(JOB_FUNCTIONS),
        'description': fake.text(),
        # 'location_policy': '',
        # 'work_contract': '',
        'min_pay': random.randint(0, 10000),
        'max_pay': random.randint(10000, 100000),
        # 'pay_rate': random.choice(PAY_RATES),
        # 'currency': '',
        'note': fake.text(),
        'status': random.choice(STATUSES),
        'company': fake.company(),
        'city': fake.city(),
        # # 'country': '',
        'region': fake.state(),
    }


@pytest.fixture()
def job_data_factory():
    def factory(updated_days_previous=None):
        return {
            'url': fake.url(),
            'source': random.choice(SOURCES),
            'job_title': fake.job(),
            # 'job_function': random.choice(JOB_FUNCTIONS),
            'description': fake.text(),
            # 'location_policy': '',
            # 'work_contract': '',
            'min_pay': random.randint(0, 10000),
            'max_pay': random.randint(10000, 100000),
            # 'pay_rate': random.choice(PAY_RATES),
            # 'currency': '',
            'note': fake.text(),
            'status': random.choice(STATUSES),
            'company': fake.company(),
            'city': fake.city(),
            # 'country': '',
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


@pytest.fixture()
def contact_form_data_factory():
    def factory(honeypot=''):
        return {'honeypot': honeypot,
                'first_name': fake.file_name(),
                'last_name': fake.file_name(),
                'email': fake.email(),
                'phone': fake.phone_number(),
                'message': fake.text()
                }
    return factory


@pytest.fixture()
def blog_post_data_factory():
    def factory():
        return {'title': fake.text(50),
                'content': fake.text(),
                'summary': fake.text(),
                'published': fake.date_time()
                }
    return factory


@pytest.fixture()
def blog_post_factory(blog_post_data_factory):
    def factory():
        data = blog_post_data_factory()
        return BlogPost(**data)
    return factory


@pytest.fixture()
def interview_data_factory(job_factory, custom_user_factory):
    def factory():
        user = custom_user_factory()
        job = job_factory(user)
        return {'user': user,
                'job': job,
                'interview_round': random.randint(1, 5),
                'start_date': fake.date_time(),
                'end_date': fake.date_time(),
                'post_code': fake.postcode(),
                'building': fake.building_number(),
                'street': fake.street_name(),
                'city': fake.city(),
                'region': fake.state(),
                # 'country': '',
                'notes': fake.text()
                }
    return factory


@pytest.fixture
def interview_factory(interview_data_factory):
    def factory():
        data = interview_data_factory()
        return Interview(**data)
    return factory


@pytest.fixture
def interview_task_data_factory(interview_factory, task_data_factory):
    def factory():
        interview = interview_factory()
        data = task_data_factory()
        data['interview'] = interview
        return data
    return factory
