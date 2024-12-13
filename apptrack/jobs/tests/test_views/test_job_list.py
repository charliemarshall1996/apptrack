
import random
from django.urls import reverse
import pytest
from core.models import Country
from jobs.views import JobListView


@pytest.mark.django_db
def test_job_list_view(client, profile_factory, job_factory, _init_choice_models):
    _init_choice_models()
    status = "OP"
    title = "Job Title"
    company = "Company"
    city = "City"
    region = "Region"
    country = random.choice(Country.objects.all())
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
    job7 = job_factory(profile)
    job7.country = country
    job7.save()

    client.force_login(user)

    jobs = [(job1, 'status', [status]),
            (job2, 'title', title),
            (job3, 'company', company),
            (job4, 'archived', 'on'),
            (job5, 'city', city),
            (job6, 'region', region),
            (job7, 'countries', [country])]

    def assert_attribute_returns_job(job, attr, value):
        data = {attr: value}
        url = reverse('jobs:list')
        response = client.get(url, data)
        assert response.status_code == 200
        assert job in response.context['view'].object_list

    for job, attr, value in jobs:
        assert_attribute_returns_job(job, attr, value)
