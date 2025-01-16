# noqa: D100
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_delete_job_view(client, job_factory, profile_factory):  # noqa: D103
    password = "securepassword"  # noqa: S105

    profile = profile_factory(password=password)
    profile.save()

    board = profile.board

    job = job_factory(profile=profile)
    job.board = board
    job.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": password}
    )

    assert response.status_code == 302

    url = reverse("jobs:delete", kwargs={"pk": job.pk})
    response = client.get(url)

    try:
        assert response.status_code == 200
    except AssertionError:
        print(response.url)

    assert job.DoesNotExist
