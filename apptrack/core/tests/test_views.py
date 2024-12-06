
from django.urls import reverse
from django.utils import timezone
import pytest


def test_home_view(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
