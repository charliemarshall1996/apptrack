# noqa: D100
import logging

import pytest

from jobs.models import (
    Job,
    JobFunction,
    LocationPolicy,
    PayRate,
    WorkContract,
)
from core.choices import StatusChoices

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_job(profile_factory, job_data_factory, company_factory):
    profile = profile_factory()
    profile.save()
    company = company_factory(profile=profile)
    company.save()
    data = job_data_factory(company=company)
    job = Job(profile=profile, **data)

    assert job.description == data["description"]
    assert job.company == company
    assert job.source == data["source"]
    assert job.city == data["city"]
    assert job.job_title == data["job_title"]
    assert job.min_pay == data["min_pay"]
    assert job.max_pay == data["max_pay"]
    assert job.note == data["note"]
    assert job.url == data["url"]
    assert job.status == data["status"]


@pytest.mark.django_db
def test_job_updated(profile_factory, job_data_factory):
    profile = profile_factory()
    profile.save()
    job = Job(profile=profile, **job_data_factory(profile=profile))

    job.save()

    original_updated = job.updated
    statuses = [
        StatusChoices.APPLIED,
        StatusChoices.SHORTLISTED,
        StatusChoices.INTERVIEW,
        StatusChoices.OFFER,
        StatusChoices.REJECTED,
        StatusChoices.CLOSED,
    ]
    i = 0
    for status in statuses:
        logger.info("status: %s", status)
        job.status = status[0]
        job.save()
        if i > 0:
            assert original_updated
            assert job.updated > original_updated
        else:
            assert job.updated
        original_updated = job.updated
        i += 1


@pytest.mark.django_db
def test_job_status_applied(profile_factory, job_data_factory):
    applied_statuses = StatusChoices.get_applied_statuses()
    data = job_data_factory()
    for status in applied_statuses:
        data["status"] = StatusChoices.OPEN[0]
        logger.info("status: %s", status)
        logger.info("jobs_data: %s", data)
        profile = profile_factory()
        profile.save()
        job = Job(profile=profile, **data)
        job.save()

        assert not job.applied
        job.status = status
        logger.info("job.status: %s", job.status)
        job.save()
        assert job.status == status
        assert job.applied


@pytest.mark.django_db
def test_job_function():
    code = "TE"
    name = "TEST"

    job_function = JobFunction(code=code, name=name)
    job_function.save()

    assert job_function.code == code
    assert job_function.name == name
    assert str(job_function) == name


@pytest.mark.django_db
def test_location_policy():
    code = "TE"
    name = "TEST"

    location_policy = LocationPolicy(code=code, name=name)
    location_policy.save()

    assert location_policy.code == code
    assert location_policy.name == name


@pytest.mark.django_db
def test_pay_rate():
    code = "TE"
    name = "TEST"

    pay_rate = PayRate(code=code, name=name)
    pay_rate.save()

    assert pay_rate.code == code
    assert pay_rate.name == name


@pytest.mark.django_db
def test_work_contract():
    code = "TE"
    name = "TEST"

    work_contract = WorkContract(code=code, name=name)
    work_contract.save()

    assert work_contract.code == code
    assert work_contract.name == name
