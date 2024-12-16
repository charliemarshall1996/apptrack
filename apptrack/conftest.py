
from datetime import timedelta
import random

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.timezone import make_aware
from faker import Faker
import pytest

from accounts.models import Profile
from core.models import Country, Currency
from core.utils import get_country_choices, get_currency_choices
from jobs.choices import (
    JobFunctionChoices,
    StatusChoices,
    SourceChoices,
    ReminderUnitChoices
)
from jobs.models import (Job,
                         Board,
                         Column,
                         Interview,
                         JobFunction)
from blog.models import BlogPost

UserModel = get_user_model()

fake = Faker()


@pytest.fixture
def _init_choice_models():
    def _init():
        for alpha_2, country in get_country_choices():
            Country.objects.get_or_create(alpha_2=alpha_2, name=country)

        for alpha_3, currency in get_currency_choices():
            Currency.objects.get_or_create(alpha_3=alpha_3, name=currency)

        for code, name in JobFunctionChoices.choices():
            JobFunction.objects.get_or_create(code=code, name=name)
    return _init


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
    def factory(password=None, email_verified=True, verification_email_sent=True):
        if verification_email_sent:
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
        else:
            return {
                'email': fake.email(),
                'email_verified': email_verified,
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

    def factory(**kwargs):
        data = custom_user_data_factory(**kwargs)
        return UserModel.objects.create_user(**data)
    return factory


@pytest.fixture
def profile_data_factory(custom_user_factory):
    def factory(user=None, **kwargs):
        return {'user': user or custom_user_factory(**kwargs),
                'email_comms_opt_in': True,
                'birth_date': timezone.now() - timedelta(days=1)}
    return factory


@pytest.fixture
def profile_factory(profile_data_factory):
    def factory(**kwargs):

        data = profile_data_factory(**kwargs)
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
        'job_function': '',
        'description': fake.text(),
        'location_policy': '',
        'work_contract': '',
        'min_pay': random.randint(0, 10000),
        'max_pay': random.randint(10000, 100000),
        'pay_rate': '',
        'currency': '',
        'note': fake.text(),
        'status': random.choice(STATUSES),
        'company': fake.company(),
        'city': fake.city(),
        'country': '',
        'region': fake.state(),
    }


@pytest.fixture()
def job_data_factory():
    def factory(**kwargs):
        COUNTRIES = [country for country in Country.objects.all()]
        CURRENCIES = [currency for currency in Currency.objects.all()]
        updated_days_previous = kwargs.pop('updated_days_previous', None)
        url = kwargs.pop('url', None)
        source = kwargs.pop('source', None)
        job_title = kwargs.pop('job_title', None)
        min_pay = kwargs.pop('min_pay', None)
        max_pay = kwargs.pop('max_pay', None)
        status = kwargs.pop('status', None)
        company = kwargs.pop("company", None)
        city = kwargs.pop("city", None)
        region = kwargs.pop("region", None)
        country = kwargs.pop("country", None)
        return {
            'url': url or fake.url(),
            'source': source or random.choice(SOURCES),
            'job_title': job_title or fake.job(),
            # 'job_function': '',
            'description': fake.text(),
            # 'location_policy': '',
            # 'work_contract': '',
            'min_pay': min_pay or random.randint(0, 10000),
            'max_pay': max_pay or random.randint(10000, 100000),
            # 'pay_rate': random.choice(PAY_RATES),
            'currency': random.choice(CURRENCIES),
            'note': fake.text(),
            'status': status or random.choice(STATUSES),
            'company': company or fake.company(),
            'city': city or fake.city(),
            'country': country or random.choice(COUNTRIES),
            'region': region or fake.state(),
            'updated': timezone.now() - timedelta(days=updated_days_previous) if updated_days_previous else timezone.now(),  # noqa
        }
    return factory


@pytest.fixture
def job_factory(job_data_factory):

    def factory(profile, **kwargs):
        data = job_data_factory(**kwargs)
        return Job(profile=profile, **data)
    return factory


@pytest.fixture
def board_data_factory(profile_factory):
    def factory(profile=None, user=None, password=None, email_verified=True, name=None, no_name=False):
        if not profile:
            profile = profile_factory(
                user=user, password=password, email_verified=email_verified)

        if no_name:
            return {'profile': profile}
        return {'profile': profile, 'name': name or fake.job()}
    return factory


@pytest.fixture()
def board_factory(board_data_factory):
    def factory(profile=None, user=None, password=None, email_verified=True, name=None, no_name=False):
        data = board_data_factory(
            profile, user, password, email_verified, name, no_name)
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
def reminder_data_factory(profile_factory):
    def factory(profile=None, emailed=False, read=False, **kwargs):
        if not profile:
            profile = profile_factory(**kwargs)
            profile.save()
        return {'profile': profile,
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
                'published': make_aware(fake.date_time())
                }
    return factory


@pytest.fixture()
def blog_post_factory(blog_post_data_factory):
    def factory():
        data = blog_post_data_factory()
        return BlogPost(**data)
    return factory


@pytest.fixture()
def interview_data_factory(job_factory, profile_factory):
    def factory(profile=None):
        if not profile:
            profile = profile_factory()
            profile.save()
        job = job_factory(profile)
        return {'profile': profile,
                'job': job,
                'round': random.randint(1, 5),
                'start_date': make_aware(fake.date_time()),
                'end_date': make_aware(fake.date_time()),
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
    def factory(**kwargs):
        data = interview_data_factory(**kwargs)
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
