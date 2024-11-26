import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from accounts.models import Profile
from accounts.utils import MessageManager

msg_mngr = MessageManager()

User = get_user_model()


@pytest.mark.django_db
def test_profile_settings_view(client, create_users):
    user = create_users["verified_user"]

    response = client.post(reverse("accounts:login"), {
        "email": user.email, "password": "securepassword"})

    assert response.status_code == 302

    print(f"user authenticated: {user.is_authenticated}")

    url = reverse('accounts:profile_settings', kwargs={"id": user.profile.id})

    # GET request should render the profile settings page
    response = client.get(url)
    assert response.status_code == 200

    assert 'user_form' in response.context
    assert 'profile_form' in response.context

    # POST request with valid data should update profile
    data = {
        'honeypot': '',
        'email': user.email,
        'first_name': 'Updated Name',
        'last_name': 'Updated Lastname',
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse(
        'accounts:profile', kwargs={'id': user.profile.id})

    # Check success message
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == msg_mngr.profile_update_success


@pytest.mark.django_db
def test_profile_settings_view_spam(client, create_users):
    user = create_users["verified_user"]

    response = client.post(reverse("accounts:login"), {
        "email": user.email, "password": "securepassword"})

    assert response.status_code == 302

    print(f"user authenticated: {user.is_authenticated}")

    url = reverse('accounts:profile_settings', kwargs={"id": user.profile.id})

    # GET request should render the profile settings page
    response = client.get(url)
    assert response.status_code == 200

    assert 'user_form' in response.context
    assert 'profile_form' in response.context

    # POST request with valid data should update profile
    data = {
        'honeypot': 'spam',
        'email': user.email,
        'first_name': 'Updated Name',
        'last_name': 'Updated Lastname',
    }

    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect after spam
    assert response.url == reverse('home')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == msg_mngr.spam


@pytest.mark.django_db
def test_profile_view(client, create_users):
    user = create_users["verified_user"]

    response = client.post(reverse("accounts:login"), {
        "email": user.email, "password": "securepassword"})

    assert response.status_code == 302
    url = reverse('accounts:profile', kwargs={'id': user.profile.id})

    # GET request should show profile details
    response = client.get(url)
    assert response.status_code == 200

    assert response.context['object'] == user


@pytest.mark.django_db
def test_logout_view(client, create_users):
    user = create_users["verified_user"]

    response = client.post(reverse("accounts:login"), {
        "email": user.email, "password": "securepassword"})

    assert response.status_code == 302
    url = reverse('accounts:logout')

    # Logout and ensure redirection to home
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_custom_login_view(client, create_users):
    user = create_users["verified_user"]

    url = reverse('accounts:login')

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # POST with valid data should log in and redirect
    data = {'honeypot': '', 'email': user.email, 'password': 'securepassword'}
    response = client.post(url, data)
    assert response.status_code == 302
    # Assuming this is the redirect
    assert response.url == reverse('jobs:board')


@pytest.mark.django_db
def test_custom_login_view_invalid_credentials(client, create_users):

    user = create_users["verified_user"]

    url = reverse('accounts:login')

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # POST with invalid credentials should show error
    data = {'honeypot': '', 'email': user.email, 'password': 'wrongpassword'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('accounts:login')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == 'Invalid login credentials'


@pytest.mark.django_db
def test_custom_login_view_spam(client, create_users):

    user = create_users["verified_user"]

    url = reverse('accounts:login')

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # Test honeypot field for spam
    data = {'honeypot': 'spam', 'email': user.email,
            'password': "securepassword"}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse('home')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == msg_mngr.spam


@pytest.mark.django_db
def test_resend_verification_email_view(client, create_users):
    user = create_users["verified_user"]

    response = client.post(reverse("accounts:login"), {
        "email": user.email, "password": "securepassword"})

    assert response.status_code == 302
    url = reverse('accounts:resend_verification_email')

    # GET request should render the resend form
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # POST with valid email should resend the email
    data = {'honeypot': '', 'email': user.email}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse('accounts:login')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "A verification email has been sent."


@pytest.mark.django_db
def test_resend_verification_email_view_spam(client, create_users):
    user = create_users["verified_user"]

    response = client.post(reverse("accounts:login"), {
        "email": user.email, "password": "securepassword"})

    assert response.status_code == 302
    url = reverse('accounts:resend_verification_email')

    # GET request should render the resend form
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # POST with valid email should resend the email
    data = {'honeypot': 'spam', 'email': user.email}

    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect after spam
    assert response.url == reverse('home')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == msg_mngr.spam


@pytest.mark.django_db
def test_password_reset_view(client, create_users):
    user = create_users["verified_user"]

    response = client.post(reverse("accounts:login"), {
        "email": user.email, "password": "securepassword"})

    assert response.status_code == 302
    url = reverse('accounts:password_reset')

    # GET request should render the password reset form
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # POST with a valid email should send a password reset email
    data = {'honeypot': '', 'email': user.email}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    messages = list(get_messages(response.wsgi_request))
    assert str(
        messages[0]) == msg_mngr.password_reset_success


@pytest.mark.django_db
def test_password_reset_view_spam(client, create_users):

    user = create_users["verified_user"]

    response = client.post(reverse("accounts:login"), {
        "email": user.email, "password": "securepassword"})

    assert response.status_code == 302
    url = reverse('accounts:password_reset')

    # GET request should render the password reset form
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # Test honeypot field for spam
    data = {'honeypot': 'spam', 'email': user.email}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect after spam
    assert response.url == reverse('home')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == msg_mngr.spam


@pytest.mark.django_db
def test_delete_account_view(client, create_users):
    user = create_users["verified_user"]

    response = client.post(reverse("accounts:login"), {
        "email": user.email, "password": "securepassword"})

    assert response.status_code == 302
    url = reverse('accounts:delete_account')

    print(f"URL: {url}")
    # GET request should render the delete confirmation page
    response = client.get(url)
    assert response.status_code == 200

    # POST request should delete the account
    response = client.post(url)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse('home')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Your account has been successfully deleted."
