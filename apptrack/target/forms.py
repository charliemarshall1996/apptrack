
from django import forms

from .models import Target


class TargetUpdateForm(forms.ModelForm):

    class Meta:
        model = Target
        fields = ["amount"]
