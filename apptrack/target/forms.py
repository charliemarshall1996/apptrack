
from django import forms

from .models import Target


class TargetUpdateForm(forms.ModelForm):

    class Meta:
        model = Target
        fields = ["amount"]

    def save(self, *args, **kwargs):
        return super().save(commit=False, *args, **kwargs)
