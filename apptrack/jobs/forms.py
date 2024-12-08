
from django import forms

from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['company',
                  'is_recruiter',
                  'job_title',
                  'job_function',
                  'city',
                  'region',
                  'country',
                  'source',
                  'url',
                  'description',
                  'location_policy',
                  'work_contract',
                  'min_pay', 'max_pay',
                  'pay_rate', 'currency',
                  'note',
                  'status']

        widgets = {
            'is_recruiter': forms.CheckboxInput()}

    def save(self, *args, **kwargs):
        return super().save(*args, commit=False, **kwargs)


class DownloadJobsForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
