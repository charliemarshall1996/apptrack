import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


@pytest.mark.django_db
def test_board_view(client, profile_factory):

    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302
    url = reverse('jobs:board')

    # GET request should show job board
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_job_view(client, board_factory, profile_factory, jobs_form_data):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    board = board_factory(user=profile.user)
    board.save()

    data = jobs_form_data

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302

    url = reverse('jobs:add_job')

    # GET request should show add job form
    response = client.get(url)
    assert response.status_code == 200
    assert 'job_form' in response.context

    # POST request with valid data should add job
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('jobs:board')
