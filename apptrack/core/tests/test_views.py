
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


@pytest.mark.django_db
def test_contact_view(client, contact_form_data_factory):
    data = contact_form_data_factory()
    url = reverse('contact')
    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_contact_view_spam(client, contact_form_data_factory):
    data = contact_form_data_factory(honeypot="spam")
    url = reverse('contact')
    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_contact_view_no_email(client, contact_form_data_factory):
    data = contact_form_data_factory()
    data['email'] = ''
    url = reverse('contact')
    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('contact')


@pytest.mark.django_db
def test_contact_view_no_first_name(client, contact_form_data_factory):
    data = contact_form_data_factory()
    data['first_name'] = ''
    url = reverse('contact')
    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('contact')


@pytest.mark.django_db
def test_contact_view_no_last_name(client, contact_form_data_factory):
    data = contact_form_data_factory()
    data['last_name'] = ''
    url = reverse('contact')
    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('contact')
