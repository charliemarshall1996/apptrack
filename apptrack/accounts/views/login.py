import logging
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_backends,
    get_user_model,
    login)
from django.dispatch import Signal
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.forms import LoginForm
from accounts.messages import AccountsMessageManager

from .utils import get_time_since_last_email, get_minutes_left_before_resend, get_can_resend


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
User = get_user_model()

user_login = Signal()


def login_non_verified_email(request, email):
    logger.info("Login request. Email: %s", email)

    try:
        user = User.objects.get(email=email)
        logger.info("User found: %s", user)
    except User.DoesNotExist:
        logger.info("User not found")
        messages.error(request, AccountsMessageManager.email_not_found)
        return redirect("accounts:login")

    if user.email_verified:
        logger.info("Email already verified")
        messages.error(request, AccountsMessageManager.email_not_verified)
        return redirect("accounts:login")

    timeout_duration = timedelta(minutes=10)

    if user.last_verification_email_sent:
        logger.info("Email already sent")
        time_since_last_email = get_time_since_last_email(
            user.last_verification_email_sent)

        can_resend = get_can_resend(
            timeout_duration, time_since_last_email)

        if can_resend:
            url = reverse(
                'accounts:resend_verification_email')
            message = AccountsMessageManager.resend_verification_email(url)
        else:
            minutes_difference = get_minutes_left_before_resend(
                time_since_last_email, timeout_duration)
            minutes_difference = round(minutes_difference)
            message = AccountsMessageManager.resend_email_wait(
                minutes_difference)
    else:
        logger.info("Email not sent")
        url = reverse(
            'accounts:resend_verification_email')
        message = AccountsMessageManager.resend_verification_email(url)

    messages.info(request, message)
    return redirect('accounts:login')


def login_view(request):
    logger.info(f"Login request. Method: {request.method}")
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['honeypot']:
                messages.error(request, AccountsMessageManager.spam)
                return redirect('core:home')

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.email_verified:
                    for backend in get_backends():
                        if user == backend.get_user(user.id):
                            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
                            break

                    user_login.send(sender=user.__class__, user=user)
                    login(request, user)
                    return redirect('accounts:dashboard')

            else:
                # Use the return value from login_non_verified_email
                return login_non_verified_email(request, email)
        else:
            messages.error(request, AccountsMessageManager.invalid_login_form)
            return redirect("accounts:login")
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)
