# noqa: D100
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_add_job_view(client, profile_factory, job_data_factory):  # noqa: D103
    password = "securepassword"  # noqa: S105

    profile = profile_factory(password=password)
    profile.save()

    data = job_data_factory()
    data["referrer"] = reverse("jobs:board")
    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": password}
    )

    assert response.status_code == 302

    url = reverse("jobs:add")

    # POST request with valid data should add job
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("jobs:board")
