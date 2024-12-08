
from django import forms

from .models import Job, StatusChoices, CountryChoices, JobFunctionChoices


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


class JobFilterForm(forms.Form):
    status = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=StatusChoices.choices(),
        required=False
    )
    title = forms.CharField(required=False, label="Job Title")
    company = forms.CharField(required=False, label="Company")
    city = forms.CharField(required=False, label="City")
    region = forms.CharField(required=False, label="Region")
    countries = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=CountryChoices.choices(),
        required=False
    )
    job_function = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=JobFunctionChoices.choices(),
        required=False
    )
