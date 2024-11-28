
from django.apps import apps
import pytest

from jobs.apps import JobsConfig


@pytest.fixture
def jobs_config():
    return {'default_auto_field': 'django.db.models.BigAutoField', 'name': 'jobs'}


@pytest.mark.django_db
def test_jobs_config(jobs_config):
    assert jobs_config["name"] == JobsConfig.name
    assert jobs_config["name"] == apps.get_app_config("jobs").name
    assert jobs_config["default_auto_field"] == JobsConfig.default_auto_field
    assert jobs_config["default_auto_field"] == apps.get_app_config(
        "jobs").default_auto_field
