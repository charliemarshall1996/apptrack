
from django.urls import reverse
from django.utils import timezone
import pytest


def test_home_view(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


def test_privacy_policy_view(client):
    url = reverse('privacy_policy')
    response = client.get(url)
    assert response.status_code == 200
