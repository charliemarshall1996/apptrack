# noqa: D100
from django.urls import reverse
import pytest

from jobs.forms import JobForm
from jobs.models import Job

# TODO: Must look at new job form


@pytest.mark.django_db
@pytest.mark.skip
def test_edit_job_view(client, job_factory, profile_factory, jobs_data, company_factory):  # noqa: D103
    password = "securepassword"  # noqa: S105

    profile = profile_factory(password=password)
    profile.save()
    company = company_factory(profile=profile)
    company.save()

    job = job_factory(profile=profile, company=company)
    job.save()

    data = JobForm(data=jobs_data).data
    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": password}
    )

    assert response.status_code == 302

    url = reverse("jobs:edit", kwargs={"pk": job.pk})
    response = client.post(url, data)

    # Get the updated job
    job = Job.objects.get(pk=job.pk)

    assert job.url == data["url"]
    assert job.source == data["source"]
    assert job.job_title == data["job_title"]
    assert job.description == data["description"]
    assert job.company == data["company"]
    assert job.min_pay == data["min_pay"]
    assert job.max_pay == data["max_pay"]
    assert job.note == data["note"]
