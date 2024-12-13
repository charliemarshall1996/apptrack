
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_add_job_view(client, profile_factory, job_data_factory, _init_choice_models):
    _init_choice_models()
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    data = job_data_factory()
    data['referrer'] = reverse('jobs:board')
    data.pop('country')
    data.pop('currency')
    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302

    url = reverse('jobs:add_job')

    # POST request with valid data should add job
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('jobs:board')
