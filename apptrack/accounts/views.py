
import logging
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from core.forms import LocationForm

from .forms import *
from .utils import get_can_resend, get_minutes_left_before_resend, get_time_since_last_email

logger = logging.getLogger(__name__)
User = get_user_model()


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        location_form = LocationForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid()\
        and location_form.is_valid():  # noqa

            if user_form.cleaned_data['honeypot']:
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(
                    request, "Your form submission was detected as spam.")
                # Redirect to prevent bot resubmission
                return redirect('home')

            location = location_form.save()
            location.save()
            user = user_form.save()
            user.email_verified = False
            user.save()
            profile = profile_form.save()
            profile.location = location
            profile.user = user
            profile.save()

            login(request, user)
            # Redirect to profile or job application list
            return redirect('jobs:board')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
        location_form = LocationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form,
                                                      'profile_form': profile_form,
                                                      'location_form': location_form})


@login_required
def profile_settings_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, instance=request.user.profile)
        location_form = LocationForm(
            request.POST, instance=request.user.profile.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():

            if user_form.cleaned_data['honeypot']:
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(
                    request, "Your form submission was detected as spam.")
                # Redirect to prevent bot resubmission
                return redirect('home')

            user = user_form.save()
            user.save()
            profile = profile_form.save()
            location = location_form.save()
            location.save()
            profile.location = location
            profile.user = user
            profile.save()

            messages.success(request, 'Your profile has been updated!')

            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        location_form = LocationForm(instance=request.user.profile.location)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'location_form': location_form
    }
    return render(request, 'accounts/profile_settings.html', context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'  # Adjust based on your template
    slug_field = 'username'  # Or 'slug' if you use a custom slug field
    slug_url_kwarg = 'slug'  # This is the URL parameter expected

    # Override get_object to use the logged-in user
    def get_object(self):
        # Return the logged-in user based on the slug
        return self.request.user


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def custom_login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['honeypot']:
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(
                    request, "Your form submission was detected as spam.")
                # Redirect to prevent bot resubmission
                return redirect('home')

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.email_verified:
                    login(request, user)
                    return redirect('jobs:board')
                else:
                    timeout_duration = timedelta(minutes=10)

                    # Example time since last email logic
                    if user.last_verification_email_sent:
                        time_since_last_email = get_time_since_last_email(
                            user.last_verification_email_sent)

                        can_resend = get_can_resend(
                            timeout_duration, time_since_last_email)

                        if can_resend:
                            resend_verification_url = reverse(
                                'accounts:resend_verification_email')

                            message = ("Please verify your email before logging in."
                                       "Please check your email for the verification link, including spam folder."
                                       f"If you need to resend the verification email, please click <a href='{resend_verification_url}'>here</a>.")
                        else:

                            minutes_difference = get_minutes_left_before_resend(
                                time_since_last_email, timeout_duration)

                            message = ("Please verify your email before logging in."
                                       "Please check your email for the verification link, including spam folder."
                                       f"You must wait {round(minutes_difference)} minutes before resending the verification email.")

                    else:
                        resend_verification_url = reverse(
                            'accounts:resend_verification_email')

                        message = ("Please verify your email before logging in."
                                   "Please check your email for the verification link, including spam folder."
                                   f"If you need to resend the verification email, please click <a href='{resend_verification_url}'>here</a>.")

                    messages.error(
                        request, message)
                    # Redirect to the login page
                    return redirect('accounts:login')
            else:
                messages.error(request, "Invalid login credentials")
                return redirect('accounts:login')
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def send_verification_email(user, request):
    from .tokens import email_verification_token  # Import the token generator
    token = email_verification_token.make_token(user)
    verification_url = request.build_absolute_uri(
        reverse('accounts:verify_email', kwargs={
                'user_id': user.id, 'token': token})
    )

    subject = "Verify your email"
    message = f"Please click the link to verify your email: {verification_url}"
    html_message = f"<p>Please click the link to verify your email: {verification_url}</p>"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
              [user.email], html_message=html_message)


def verify_email(request, user_id, token):
    from .tokens import email_verification_token  # Import the token generator
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, id=user_id)

    if email_verification_token.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(
            request, 'Your email has been verified. You can now log in.')
        return redirect('accounts:login')
    else:
        messages.error(
            request, 'The verification link is invalid or has expired.')
        return redirect('accounts:login')


def resend_verification_email(request):
    if request.method == 'POST':
        form = ResendVerificationEmailForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['honeypot']:
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(
                    request, "Your form submission was detected as spam.")
                # Redirect to prevent bot resubmission
                return redirect('home')
            email = form.cleaned_data['email']

            # Look up the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(
                    request, "No user found with that email address.")
                return redirect('accounts:resend_verification_email')

            # Define timeout duration (10 minutes here)
            timeout_duration = timedelta(minutes=10)

            # Check if a verification email has already been sent and enforce the timeout
            if user.last_verification_email_sent:
                time_since_last_email = get_time_since_last_email(
                    user.last_verification_email_sent)
                timeout_duration = timedelta(minutes=10)
                minutes_difference = get_minutes_left_before_resend(
                    time_since_last_email, timeout_duration)

                if time_since_last_email < timeout_duration:
                    messages.error(
                        request, f"Please wait {minutes_difference} before resending the verification email.")
                    return redirect('accounts:resend_verification_email')

            # Send verification email and update `last_verification_email_sent`
            send_verification_email(user, request)
            user.last_verification_email_sent = timezone.now()
            user.save()

            messages.success(request, "A verification email has been sent.")
            # Redirect to a suitable page like login or home
            return redirect('accounts:login')
    else:
        form = ResendVerificationEmailForm()

    return render(request, 'accounts/resend_verification_email.html', {'form': form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


@login_required
def delete_account_view(request):
    # Handle the POST request (when the user confirms the deletion)
    if request.method == 'POST':
        user = request.user  # Get the logged-in user
        user.delete()  # Delete the user account
        messages.success(
            request, "Your account has been successfully deleted.")
        return redirect('home')  # Redirect to the homepage after deletion

    # Render the confirmation page
    return render(request, 'accounts/delete_account.html')
