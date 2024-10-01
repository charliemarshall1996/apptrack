from django import forms
from django.core.validators import EmailValidator

class ContactForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(validators=[EmailValidator()])
    phone = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea)