
import logging
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_backends,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic.detail import DetailView


from .forms import (
    UserUpdateForm,
    UserRegistrationForm,
    UserLoginForm,
    ProfileRegistrationForm,
    ProfileUpdateForm,
    ResendVerificationEmailForm,
    PasswordResetForm
)
from .models import Profile
from .utils import (get_can_resend, get_minutes_left_before_resend, get_time_since_last_email,
                    MessageManager)

logger = logging.getLogger(__name__)
User = get_user_model()


@login_required
def profile_settings_view(request, id):
    # Fetch the profile using the slug
    profile = get_object_or_404(Profile, id=id)

    # Check if the logged-in user owns the profile, otherwise redirect
    if profile.user != request.user:
        messages.error(
            request, "You are not authorized to view or edit this profile.")
        return redirect('home')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            if user_form.cleaned_data['honeypot']:
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(
                    request, MessageManager.spam)
                return redirect('home')

            user = user_form.save()
            profile = profile_form.save()
            profile.user = user
            profile.save()

            messages.success(request, MessageManager.profile_update_success)

            return redirect('accounts:profile', id=profile.id)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    }
    return render(request, 'accounts/profile_settings.html', context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'  # Adjust based on your template
    slug_field = 'id'  # Or 'slug' if you use a custom slug field
    slug_url_kwarg = 'slug'  # This is the URL parameter expected

    # Override get_object to use the logged-in user
    def get_object(self):
        # Return the logged-in user based on the slug
        return self.request.user


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def login_non_verified_email(request, email):
    logger.debug(f"Email: {email}")
    try:
        user = User.objects.get(email=email)
        logger.debug(f"User: {user}")
    except User.DoesNotExist:
        logger.debug("User does not exist")
        messages.error(request, "Invalid login credentials")
        return redirect("accounts:login")

    if user.email_verified:
        messages.error(request, "Invalid login credentials")
        return redirect("accounts:login")

    timeout_duration = timedelta(minutes=10)

    if user.last_verification_email_sent:
        time_since_last_email = get_time_since_last_email(
            user.last_verification_email_sent)

        can_resend = get_can_resend(
            timeout_duration, time_since_last_email)

        if can_resend:
            resend_verification_url = reverse(
                'accounts:resend_verification_email')
            message = (f"""
            Please verify your email before logging in.
            Please check your email for the verification link, including spam folder.
            If you need to resend the verification email, please click <a href='{reverse(
            'accounts:resend_verification_email')}'>here</a>.
            """)
        else:
            minutes_difference = get_minutes_left_before_resend(
                time_since_last_email, timeout_duration)

            message = ("""
                Please verify your email before logging in.
                Please check your email for the verification link, including spam folder.
                You must wait {} minutes before resending the verification email.
                """.format(round(minutes_difference)))
    else:
        resend_verification_url = reverse('accounts:resend_verification_email')
        message = ("""
            Please verify your email before logging in.
            Please check your email for the verification link, including spam folder.
            If you need to resend the verification email, please click
            <a href='{}'>here</a>.
            """.format(resend_verification_url))

    messages.error(request, message)
    return redirect('accounts:login')


def custom_login_view(request):
    logger.debug(f"Login request. Method: {request.method}")
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            logger.debug("Form is valid")
            if form.cleaned_data['honeypot']:
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(request, MessageManager.spam)
                # Redirect to prevent bot resubmission
                return redirect('home')

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                logger.debug(f"User exitsts for email: {email}")
                if user.email_verified:
                    for backend in get_backends():
                        if user == backend.get_user(user.id):
                            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
                            break

                    login(request, user)
                    return redirect('jobs:board')

            else:
                # Use the return value from login_non_verified_email
                return login_non_verified_email(request, email)
        else:
            logger.debug(f"Form is not valid {form.errors}")
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


def send_password_reset_email(user, request):
    from .tokens import password_reset_token  # Import the token generator
    token = password_reset_token.make_token(user)
    password_reset_url = request.build_absolute_uri(
        reverse('accounts:password_reset_confirm', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token})
    )

    subject = "Reset your password"
    message = f"Please click the link to reset your password: {password_reset_url}"
    html_message = f"<p>Please click the link to reset your password: {password_reset_url}</p>"
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
                    request, MessageManager.spam)
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


def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():

            if form.cleaned_data['honeypot']:
                logger.debug("Honeypot field filled")
                # Honeypot field should be empty.
                # If it's filled, treat it as spam.
                messages.error(
                    request, MessageManager.spam)
                # Redirect to prevent bot resubmission
                return redirect('home')

            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                send_password_reset_email(user, request)
                messages.success(
                    request, MessageManager.password_reset_success)
                return redirect("accounts:password_reset")
            else:
                messages.error(
                    request, MessageManager.user_not_found)
            return redirect('accounts:password_reset')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})


@ login_required
def delete_account_view(request):
    # Handle the POST request (when the user confirms the deletion)
    if request.method == 'POST':
        user = request.user  # Get the logged-in user
        user.profile.delete()  # Delete the user's profile
        user.delete()  # Delete the user account
        messages.success(
            request, "Your account has been successfully deleted.")
        return redirect('home')  # Redirect to the homepage after deletion

    # Render the confirmation page
    return render(request, 'accounts/delete_account.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            if user_form.cleaned_data['honeypot']:
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(
                    request, MessageManager.spam)
                # Redirect to prevent bot resubmission
                return redirect('home')

            user = user_form.save()
            user.email_verified = False
            user.save()
            profile = profile_form.save()
            profile.user = user
            profile.save()

            # Send verification email
            send_verification_email(user, request)

            messages.success(
                request, "Your account has been created.\nPlease check your email to verify your account.")

            # Redirect to profile or job application list
            return redirect('accounts:login')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form,
                                                      'profile_form': profile_form})
