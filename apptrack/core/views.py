from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.http import JsonResponse

import pycountry


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
    
# View to load regions for a selected country
def get_subdivisions(request, country_code):
    try:
        subdivisions = pycountry.subdivisions.get(country_code=country_code)
        regions = [{"code": sub.code, "name": sub.name} for sub in subdivisions]
    except KeyError:
        regions = []
    return JsonResponse({"regions": regions})

# View to load cities for a selected region (you can use an API or a static dataset)
def load_cities(request):
    region_code = request.GET.get('region_code')
    # Example static data (in real applications, use a database or API)
    cities = {
        'US-CA': ['Los Angeles', 'San Francisco', 'San Diego'],  # Cities in California
        'GB-ENG': ['London', 'Manchester', 'Liverpool']  # Cities in England
    }
    cities_in_region = cities.get(region_code, [])
    
    return JsonResponse({'cities': cities_in_region})

def privacy_policy_view(request):
    return render(request, 'core/privacy_policy.html')