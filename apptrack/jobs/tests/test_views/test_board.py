from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_board_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {"email": profile.user.email, "password": PASSWORD}
    )

    assert response.status_code == 302
    url = reverse("jobs:board")

    # GET request should show job board
    response = client.get(url)
    assert response.status_code == 200
