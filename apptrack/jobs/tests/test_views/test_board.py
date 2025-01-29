# noqa: D100
from django.urls import reverse
import pytest


@pytest.mark.skip
def test_board_view(client, profile_factory):  # noqa: D103
    password = "securepassword"  # noqa: S105

    profile = profile_factory(password=password)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": password}
    )

    assert response.status_code == 302
    url = reverse("jobs:board")

    # GET request should show job board
    response = client.get(url)
    assert response.status_code == 200
