
import pytest
from jobs.forms import JobForm


@pytest.mark.django_db
def test_job_form(jobs_form_data, custom_user_factory):
    user = custom_user_factory()
    form = JobForm(data=jobs_form_data)
    assert form.is_valid()
    job = form.save()
    job.user = user
    assert job.url == jobs_form_data['url']
    assert job.source == jobs_form_data['source']
    assert job.job_title == jobs_form_data['job_title']
    assert job.description == jobs_form_data['description']
    assert job.min_pay == jobs_form_data['min_pay']
    assert job.max_pay == jobs_form_data['max_pay']
    assert job.note == jobs_form_data['note']
    assert job.status == jobs_form_data['status']
    job.save()
    job.delete()
