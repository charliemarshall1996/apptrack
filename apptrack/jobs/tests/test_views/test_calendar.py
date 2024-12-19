from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_calendar_view(client, profile_factory):
    profile = profile_factory()
    profile.save()
    url = reverse("jobs:calendar")
    client.force_login(user=profile.user)
    response = client.get(url)

    assert response.status_code == 200
    assert "user_id" in response.context
    assert "add_form" in response.context
    assert "add_reminder_form" in response.context
    assert "interviews" in response.context
    assert "all_interviews" in response.context
    assert "edit_forms" in response.context
