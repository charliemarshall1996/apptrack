
from django import forms
from django.core.validators import EmailValidator

from .models import Locations


class LocationForm(forms.ModelForm):
    class Meta:
        model = Locations
        fields = ['country', 'region', 'city']

    def save(self, *args, **kwargs):
        return super().save(*args, commit=False, **kwargs)


class ContactForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(validators=[EmailValidator()])
    phone = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea)
