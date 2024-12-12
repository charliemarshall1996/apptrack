

import pytest
from django.urls import reverse
from django.contrib.messages import get_messages

from accounts.messages import AccountsMessageManager


@pytest.mark.django_db
def test_resend_verification_email_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302
    url = reverse('accounts:resend_verification_email')

    # GET request should render the resend form
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # POST with valid email should resend the email
    data = {'honeypot': '', 'email': profile.user.email}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse('accounts:login')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "A verification email has been sent."


@pytest.mark.django_db
def test_resend_verification_email_view_spam(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302
    url = reverse('accounts:resend_verification_email')

    # GET request should render the resend form
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # POST with valid email should resend the email
    data = {'honeypot': 'spam', 'email': profile.user.email}

    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect after spam
    assert response.url == reverse('core:home')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.spam
