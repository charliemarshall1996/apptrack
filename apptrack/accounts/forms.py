from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1',
                  'password2', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["password1"].required = True
        self.fields["password2"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    def save(self):
        return super().save(commit=False)


class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'gender']

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self) -> Profile:
        return super().save(commit=False)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []
