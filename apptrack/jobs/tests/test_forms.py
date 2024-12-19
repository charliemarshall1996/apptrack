import pytest
from core.models import Country
from jobs.forms import JobForm, JobFilterForm, AddInterviewForm
from jobs.models import JobFunction, Interview


@pytest.mark.django_db
def test_job_form(jobs_form_data, profile_factory):
    profile = profile_factory()
    profile.save()
    form = JobForm(data=jobs_form_data)
    assert form.is_valid()
    job = form.save()
    job.profile = profile
    assert job.url == jobs_form_data["url"]
    assert job.source == jobs_form_data["source"]
    assert job.job_title == jobs_form_data["job_title"]
    assert job.description == jobs_form_data["description"]
    assert job.min_pay == jobs_form_data["min_pay"]
    assert job.max_pay == jobs_form_data["max_pay"]
    assert job.note == jobs_form_data["note"]
    assert job.status == jobs_form_data["status"]
    job.save()
    job.delete()


@pytest.mark.django_db
def test_add_interview_form(interview_data_factory):
    # initialise data
    data = interview_data_factory()
    data["job"].save()
    data.pop("profile")

    form = AddInterviewForm(data=data)

    try:
        interview = form.save()
        assert isinstance(interview, Interview)
    except (AssertionError, ValueError):
        print(form.errors)
        raise AssertionError


@pytest.mark.django_db
def test_job_filter_form_init():
    form = JobFilterForm()

    assert form.fields["countries"].choices == [
        (country.alpha_2, country.name) for country in Country.objects.all()
    ]

    assert form.fields["job_functions"].choices == [
        (job_function.code, job_function.name)
        for job_function in JobFunction.objects.all()
    ]
