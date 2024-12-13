
import logging

from django.contrib import messages
from django.shortcuts import render, redirect

from accounts.forms import UserRegistrationForm, ProfileRegistrationForm
from accounts.mail import AccountsEmailManager
from accounts.messages import AccountsMessageManager

logger = logging.getLogger(__name__)

email_manager = AccountsEmailManager()


def registration_view(request):
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
            email_manager.mail_verification(request, user)

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
