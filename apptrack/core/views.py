from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


from .forms import ContactForm

def home_view(request):
    return render(request, 'core/index.html')

class ContactView(SuccessMessageMixin, FormView):
    form_class = ContactForm        # The form class
    success_url = reverse_lazy('contact')  # Redirect URL after successful form submission
    success_message = "Your message has been sent successfully!"  # Success message
    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean_honeypot(self):
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError("Bot detected!")
        return honeypot

    def form_valid(self, form):
        # Get form data
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        phone = form.cleaned_data['phone']

        # Compose email subject and message
        subject = f"Contact Form Submission from {first_name} {last_name}"
        email_message = f"Name: {first_name} {last_name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"

        # Send email to the admin (or your email)
        send_mail(
            subject,
            email_message,
            email,  # From email
            ['charlie.marshall1996@gmail.com'],  # To email
            fail_silently=False,
        )

        return super().form_valid(form)