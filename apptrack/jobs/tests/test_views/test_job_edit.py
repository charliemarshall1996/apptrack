
from django.urls import reverse
import pytest

from jobs.forms import JobForm
from jobs.models import Job


@pytest.mark.django_db
def test_edit_job_view(client, job_factory, profile_factory, jobs_data, _init_choice_models):
    _init_choice_models()
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    board = profile.board
    board.save()

    job = job_factory(profile=profile)
    job.board = board
    job.save()

    data = JobForm(data=jobs_data).data
    data['editJobReferrer'] = reverse('jobs:board')
    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302

    url = reverse("jobs:edit_job", kwargs={"pk": job.pk})
    response = client.post(url, data)

    # Get the updated job
    job = Job.objects.get(pk=job.pk)

    assert job.url == data['url']
    assert job.source == data['source']
    assert job.job_title == data['job_title']
    assert job.description == data['description']
    assert job.company == data["company"]
    assert job.min_pay == data['min_pay']
    assert job.max_pay == data["max_pay"]
    assert job.note == data["note"]
