
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
from django.dispatch import Signal
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic.detail import DetailView

from jobs.models import (Job, Task, Interview)

from .forms import (
    UserUpdateForm,
    UserRegistrationForm,
    UserLoginForm,
    ProfileRegistrationForm,
    ProfileUpdateForm,
    ResendVerificationEmailForm,
    PasswordResetForm,
    TargetUpdateForm
)
from .messages import AccountsMessageManager
from .models import Profile, Target
from .utils import (get_can_resend,
                    get_minutes_left_before_resend,
                    get_time_since_last_email)


logger = logging.getLogger(__name__)
User = get_user_model()

user_login = Signal()


@login_required
def profile_settings_view(request, id):
    # Fetch the profile using the slug
    profile = get_object_or_404(Profile, id=id)
    target = get_object_or_404(Target, profile=profile)

    # Check if the logged-in user owns the profile, otherwise redirect
    if profile.user != request.user:
        messages.error(
            request, "You are not authorized to view or edit this profile.")
        return redirect('core:home')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        target_form = TargetUpdateForm(request.POST, instance=target)

        if user_form.is_valid() and profile_form.is_valid() and target_form.is_valid():

            user = user_form.save()
            user.save()
            target = target_form.save()
            target.save()
            profile = profile_form.save()
            profile.user = user
            profile.target = target
            profile.save()

            messages.success(
                request, AccountsMessageManager.profile_update_success)

            return redirect('accounts:profile', id=profile.id)
        else:
            if not profile_form.is_valid():
                errors = profile_form.errors.as_data()
                if errors.get('birth_date'):
                    messages.error(
                        request, AccountsMessageManager.invalid_birth_date)

            messages.error(
                request, f"Invalid form {profile_form.errors} {user_form.errors} {target_form.errors}")
            return redirect("accounts:profile", id=profile.id)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        target, created = Target.objects.get_or_create(profile=profile)
        target_form = TargetUpdateForm(instance=target)

    context = {
        'user_id': request.user.id,
        'target_form': target_form,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        return context


@login_required
def logout_view(request):
    logout(request)
    return redirect('core:home')


def login_non_verified_email(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, AccountsMessageManager.email_not_found)
        return redirect("accounts:login")

    if user.email_verified:
        messages.error(request, AccountsMessageManager.email_not_verified)
        return redirect("accounts:login")

    timeout_duration = timedelta(minutes=10)

    if user.last_verification_email_sent:
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
        url = reverse(
            'accounts:resend_verification_email')
        message = AccountsMessageManager.resend_verification_email(url)

    messages.error(request, message)
    return redirect('accounts:login')


def custom_login_view(request):
    logger.debug(f"Login request. Method: {request.method}")
    if request.method == "POST":
        form = UserLoginForm(request.POST)

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
                    return redirect('jobs:board')

            else:
                # Use the return value from login_non_verified_email
                return login_non_verified_email(request, email)
        else:
            messages.error(request, AccountsMessageManager.invalid_login_form)
            return redirect("accounts:login")
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
            request, AccountsMessageManager.email_verified)
        return redirect('accounts:login')


def resend_verification_email(request):
    if request.method == 'POST':
        form = ResendVerificationEmailForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['honeypot']:
                messages.error(
                    request, AccountsMessageManager.spam)

                return redirect('core:home')
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(
                    request, AccountsMessageManager.email_not_found)
                return redirect('accounts:resend_verification_email')

            timeout_duration = timedelta(minutes=10)

            if user.last_verification_email_sent:
                time_since_last_email = get_time_since_last_email(
                    user.last_verification_email_sent)
                timeout_duration = timedelta(minutes=10)
                minutes_difference = get_minutes_left_before_resend(
                    time_since_last_email, timeout_duration)

                if time_since_last_email < timeout_duration:
                    messages.info(
                        request,
                        AccountsMessageManager.resend_email_wait(minutes_difference))
                    return redirect('accounts:resend_verification_email')

            send_verification_email(user, request)
            user.last_verification_email_sent = timezone.now()
            user.save()

            messages.success(
                request, AccountsMessageManager.email_verification_sent)
            return redirect('accounts:login')
    else:
        form = ResendVerificationEmailForm()

    return render(request, 'accounts/resend_verification_email.html', {'form': form})


def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():

            if form.cleaned_data['honeypot']:
                messages.error(
                    request, AccountsMessageManager.spam)
                return redirect('core:home')

            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                send_password_reset_email(user, request)
                messages.success(
                    request, AccountsMessageManager.password_reset_success)
                return redirect("accounts:password_reset")
            else:
                messages.error(
                    request, AccountsMessageManager.email_not_found)
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
            request, AccountsMessageManager.account_deleted_success)
        return redirect('core:home')  # Redirect to the homepage after deletion

    # Render the confirmation page
    return render(request, 'accounts/delete_account.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            if user_form.cleaned_data['honeypot']:
                messages.error(
                    request, AccountsMessageManager.spam)
                return redirect('core:home')

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
            if user_form.errors:
                error_data = user_form.errors.as_data()
                email_error = error_data.get("email")
                password_error = error_data.get(
                    "password2") or error_data.get("password1")
                logger.info("User form errors: %s", error_data)
                if email_error:
                    logger.info("Email address is invalid")
                    messages.error(
                        request, AccountsMessageManager.invalid_email)
                if password_error:
                    messages.error(
                        request, AccountsMessageManager.invalid_password)

            return redirect('accounts:register')

    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form,
                                                      'profile_form': profile_form})


def home_view(request):
    jobs = Job.objects.filter(
        user=request.user, archived=False).order_by("updated").all()[:10]
    interviews = Interview.objects.filter(
        user=request.user, start_date__gte=timezone.now()).order_by("start_date").all()[:10]
    tasks = Task.objects.filter(
        user=request.user).order_by("priority").all()[:10]

    context = {"user_id": request.user.id, "jobs": jobs,
               "interviews": interviews, "tasks": tasks}
    return render(request, "accounts/dashboard.html", context)
