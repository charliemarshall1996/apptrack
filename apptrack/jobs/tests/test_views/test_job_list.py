# noqa: D100
from django.urls import reverse
import pytest

# TODO: Must look at new jobs filter form


@pytest.mark.django_db
@pytest.mark.skip
def test_job_list_view(client, profile_factory, job_factory, company_factory):
    """Ensures the jobs list view works over a variety of filters."""
    status = "OP"
    title = "Job Title"
    company = company_factory()
    company.save()
    city = "City"
    region = "Region"
    profile = profile_factory()
    profile.save()
    user = profile.user
    job1 = job_factory(profile)
    job1.status = status
    job1.save()
    job2 = job_factory(profile)
    job2.job_title = title
    job2.save()
    job3 = job_factory(profile)
    job3.company = company
    job3.save()
    job4 = job_factory(profile)
    job4.archived = True
    job4.save()
    job5 = job_factory(profile)
    job5.city = city
    job5.save()
    job6 = job_factory(profile)
    job6.region = region
    job6.save()

    client.force_login(user)

    jobs = [
        (job1, "status", [status]),
        (job2, "title", title),
        (job3, "company", company),
        (job4, "archived", "on"),
        (job5, "city", city),
        (job6, "region", region),
    ]

    def assert_attribute_returns_job(job, attr, value):
        data = {attr: value}
        url = reverse("jobs:list")
        response = client.get(url, data)
        assert response.status_code == 200
        assert job in response.context["view"].object_list

    for job, attr, value in jobs:
        if attr == 'company':
            value = value.name
        assert_attribute_returns_job(job, attr, value)
