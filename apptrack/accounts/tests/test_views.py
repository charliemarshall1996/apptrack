import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from accounts.tokens import email_verification_token
from accounts.utils import MessageManager

msg_mngr = MessageManager()

User = get_user_model()


@pytest.mark.django_db
def test_profile_settings_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302

    url = reverse('accounts:profile_settings', kwargs={
                  "id": profile.user.profile.id})

    # GET request should render the profile settings page
    response = client.get(url)
    assert response.status_code == 200

    assert 'user_form' in response.context
    assert 'profile_form' in response.context

    # POST request with valid data should update profile
    data = {
        'honeypot': '',
        'email': profile.user.email,
        'first_name': 'Updated Name',
        'last_name': 'Updated Lastname',
        'daily_target': 100
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse(
        'accounts:profile', kwargs={'id': profile.user.profile.id})

    # Check success message
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == msg_mngr.profile_update_success


@pytest.mark.django_db
def test_profile_settings_view_invalid_profile(client, profile_factory, custom_user_factory):
    PASSWORD = "securepassword"

    user_profile = profile_factory(password=PASSWORD)
    user_profile.save()
    profile = profile_factory(password=PASSWORD)
    profile.save()

    assert user_profile
    assert profile

    response = client.post(reverse("accounts:login"), {
        "email": user_profile.user.email, "password": PASSWORD})

    assert response.status_code == 302
    print(f"Login response {list(get_messages(response.wsgi_request))}")
    print(f"user authenticated: {user_profile.user.is_authenticated}")

    url = reverse('accounts:profile_settings', kwargs={
                  "id": profile.user.profile.id})

    response = client.get(url)
    # assert response.status_code == 302

    # Check success message
    messages = list(get_messages(response.wsgi_request))
    print(messages)
    assert str(
        messages[0]) == "You are not authorized to view or edit this profile."


@pytest.mark.django_db
def test_profile_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302
    url = reverse('accounts:profile', kwargs={'id': profile.user.profile.id})

    # GET request should show profile details
    response = client.get(url)
    assert response.status_code == 200

    assert response.context['object'] == profile.user


@pytest.mark.django_db
def test_logout_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302
    url = reverse('accounts:logout')

    # Logout and ensure redirection to home
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('core:home')


@pytest.mark.django_db
def test_custom_login_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    url = reverse('accounts:login')

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # POST with valid data should log in and redirect
    data = {'honeypot': '', 'email': profile.user.email,
            'password': PASSWORD}
    response = client.post(url, data)
    assert response.status_code == 302
    # Assuming this is the redirect
    assert response.url == reverse('jobs:board')


@pytest.mark.django_db
def test_custom_login_view_unverified_email(client, profile_factory):
    PASSWORD = "securepassword"
    URL = reverse('accounts:login')
    MESSAGE = f"""
            Please verify your email before logging in.
            Please check your email for the verification link, including spam folder.
            If you need to resend the verification email, please click <a href='{reverse(
            'accounts:resend_verification_email')}'>here</a>.
            """
    profile = profile_factory(password=PASSWORD, email_verified=False)
    profile.save()

    response = client.get(URL)
    assert response.status_code == 200
    assert 'form' in response.context

    data = {'honeypot': '', 'email': profile.user.email, "password": PASSWORD}
    response = client.post(URL, data)
    assert response.status_code == 302
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == MESSAGE


@pytest.mark.django_db
def test_custom_login_view_invalid_credentials(client, profile_factory):

    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    url = reverse('accounts:login')

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # POST with invalid credentials should show error
    data = {'honeypot': '', 'email': profile.user.email,
            'password': 'wrongpassword'}
    response = client.post(url, data)
    # assert response.status_code == 302
    assert response.url == reverse('accounts:login')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == 'Invalid login credentials'


@pytest.mark.django_db
def test_custom_login_view_spam(client, profile_factory):

    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    url = reverse('accounts:login')

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # Test honeypot field for spam
    data = {'honeypot': 'spam', 'email': profile.user.email,
            'password': "securepassword"}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse('core:home')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == msg_mngr.spam


@pytest.mark.django_db
def test_custom_login_view_email_does_not_exist(client, profile_factory):

    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    url = reverse('accounts:login')

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # Test honeypot field for spam
    data = {'honeypot': '', 'email': "a@b.com",
            'password': PASSWORD}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse('accounts:login')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Invalid login credentials"


@pytest.mark.django_db
def test_custom_login_view_invalid_form(client, profile_factory):

    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    url = reverse('accounts:login')

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # Test honeypot field for spam
    data = {'honeypot': '', 'email': "a@b.c",
            'password': PASSWORD}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse('accounts:login')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Login form is not valid"


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
    assert str(messages[0]) == msg_mngr.spam


@pytest.mark.django_db
def test_password_reset_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302
    url = reverse('accounts:password_reset')

    # GET request should render the password reset form
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # POST with a valid email should send a password reset email
    data = {'honeypot': '', 'email': profile.user.email}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    messages = list(get_messages(response.wsgi_request))
    assert str(
        messages[0]) == msg_mngr.password_reset_success


@pytest.mark.django_db
def test_password_reset_view_spam(client, profile_factory):

    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302
    url = reverse('accounts:password_reset')

    # GET request should render the password reset form
    response = client.get(url)
    assert response.status_code == 200

    assert 'form' in response.context

    # Test honeypot field for spam
    data = {'honeypot': 'spam', 'email': profile.user.email}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect after spam
    assert response.url == reverse('core:home')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == msg_mngr.spam


@pytest.mark.django_db
def test_delete_account_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302
    url = reverse('accounts:delete_account')

    print(f"URL: {url}")
    # GET request should render the delete confirmation page
    response = client.get(url)
    assert response.status_code == 200

    # POST request should delete the account
    response = client.post(url)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse('core:home')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Your account has been successfully deleted."


@pytest.mark.django_db
def test_register_view_valid(client, user_registration_form_data):
    email = user_registration_form_data['email']

    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200

    url = reverse('accounts:register')

    # GET request should render the register form
    response = client.post(url, user_registration_form_data)
    user = User.objects.get(email=email)
    assert response.status_code == 302
    assert response.url == reverse('accounts:login')
    assert user
    assert user.profile


@pytest.mark.django_db
def test_register_view_invalid_email(client, user_registration_form_data):
    user_registration_form_data['email'] = "invalid_email"

    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200

    url = reverse('accounts:register')

    # GET request should render the register form
    response = client.post(url, user_registration_form_data)
    assert response.status_code == 302
    assert response.url == reverse('accounts:register')

    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Please enter a valid email address."


@pytest.mark.django_db
def test_register_view_spam(client, user_registration_form_data):

    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200
    user_registration_form_data["honeypot"] = "spam"
    url = reverse('accounts:register')

    # GET request should render the register form
    response = client.post(url, user_registration_form_data)
    assert response.status_code == 302
    assert response.url == reverse('core:home')

    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == msg_mngr.spam


@pytest.mark.django_db
def test_register_view_mismatched_password(client, user_registration_form_data):
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200
    user_registration_form_data["password2"] = "incorrect_password"
    url = reverse('accounts:register')

    # GET request should render the register form
    response = client.post(url, user_registration_form_data)
    assert response.status_code == 302
    assert response.url == reverse('accounts:register')

    messages = list(get_messages(response.wsgi_request))
    print(str(messages[0]))
    assert str(messages[0]) == "Please enter a valid password."


@pytest.mark.django_db
def test_register_view_password_too_common(client, user_registration_form_data):
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200
    user_registration_form_data["password1"] = "password1"
    user_registration_form_data["password2"] = "password1"
    url = reverse('accounts:register')

    # GET request should render the register form
    response = client.post(url, user_registration_form_data)
    assert response.status_code == 302
    assert response.url == reverse('accounts:register')

    messages = list(get_messages(response.wsgi_request))
    print(str(messages[0]))
    assert str(messages[0]) == "Please enter a valid password."


@pytest.mark.django_db
def test_email_verification_view(client, custom_user_factory):
    user = custom_user_factory(email_verified=False)
    token = email_verification_token.make_token(user)

    url = reverse('accounts:verify_email', kwargs={
                  'user_id': user.id, 'token': token})
    response = client.get(url)
    user = User.objects.get(id=user.id)
    assert response.status_code == 302
    assert response.url == reverse('accounts:login')
    assert user.email_verified
