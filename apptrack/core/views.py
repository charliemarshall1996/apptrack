
import logging

from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import ContactForm

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

User = get_user_model()


def home_view(request):
    return render(request, 'core/index.html')


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['honeypot']:
                logger.debug("Honeypot field filled")
                # Honeypot field should be empty. If it's filled, treat it as spam.
                messages.error(request, "Spam detected")
                # Redirect to prevent bot resubmission
                return redirect('core:home')

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            phone = form.cleaned_data['phone']

            html_message = f"""
            <p><strong>First Name:</strong> {first_name}</p>
            <p><strong>Last Name:</strong> {last_name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone:</strong> {phone}</p>
            <p><strong>Message:</strong></p>
            <br>
            <p>{message}</p>
            """

            # Compose email subject and message
            subject = f"Contact Form Submission from {first_name} {last_name}"

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # From email
                ['charlie.marshall1996@gmail.com'],  # To email
                fail_silently=False,
                html_message=html_message
            )

            messages.success(
                request, "Your message has been sent successfully!")
            return redirect('core:home')
        else:
            logger.debug("Invalid form data")
            logger.debug("Errors: %s", form.errors)
            messages.error(request, "Please fill out the form correctly.")
            return redirect('core:contact')
    else:
        form = ContactForm()
        return render(request, 'core/contact.html', {'form': form})


def privacy_policy_view(request):
    return render(request, 'core/privacy_policy.html')
