# noqa: D100
from django.urls import reverse
import pytest

from jobs.models import Settings


@pytest.mark.django_db
def test_settings_view(client, profile_factory):  # noqa: D103
    password = "securepassword"  # noqa: S105

    profile = profile_factory(password=password)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": password}
    )

    assert response.status_code == 302
    url = reverse("jobs:settings")

    # GET request should show job settings page
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_settings_view_updated(client, profile_factory):
    password = "securepassword"  # noqa: S105

    profile = profile_factory(password=password)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": password}
    )

    assert response.status_code == 302
    url = reverse("jobs:settings")

    # GET request should show job settings page
    response = client.get(url)
    assert response.status_code == 200

    # POST request with valid data should update job settings
    data = {"auto_archive": False, "archive_after_weeks": 4}
    response = client.post(url, data)
    assert response.status_code == 302

    settings = Settings.objects.get(profile=profile)
    assert not settings.auto_archive
    assert settings.archive_after_weeks == 4
