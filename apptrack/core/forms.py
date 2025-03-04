from django import forms
from django.core.validators import EmailValidator


class ContactForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(validators=[EmailValidator()], required=True)
    phone = forms.CharField(max_length=25)
    message = forms.CharField(widget=forms.Textarea)
