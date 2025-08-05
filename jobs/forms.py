
from django import forms
from core.models import Country
from .models import Job, StatusChoices, JobFunction, Settings


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = [
            "is_recruiter",
            "job_title",
            "job_function",
            "city",
            "region",
            "country",
            "source",
            "url",
            "description",
            "location_policy",
            "work_contract",
            "min_pay",
            "max_pay",
            "pay_rate",
            "currency",
            "note",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        is_recruiter = cleaned_data.get('is_recruiter', False)
        profile = self.profile
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.profile = self.profile
        if commit:
            instance.save()
        return instance


class DownloadJobsForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))


class JobFilterForm(forms.Form):
    INCLUDE = "in"
    EXCLUDE = "ex"
    ONLY = "on"

    ARCHIVED_CHOICES = [
        (INCLUDE, "Include"),
        (EXCLUDE, "Exclude"),
        (ONLY, "Only"),
    ]

    status = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=StatusChoices.choices(),  # Assuming StatusChoices remains a class
        required=False,
    )
    title = forms.CharField(required=False, label="Job Title")
    city = forms.CharField(required=False, label="City")
    region = forms.CharField(required=False, label="Region")
    archived = forms.ChoiceField(
        choices=ARCHIVED_CHOICES, required=False, initial=INCLUDE
    )

    # Dynamically populate choices for countries
    countries = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, required=False
    )

    # Dynamically populate choices for job functions
    job_functions = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate the choices for countries dynamically
        self.fields["countries"].choices = [
            (country.alpha_2, country.name) for country in Country.objects.all()
        ]

        # Populate the choices for job functions dynamically
        self.fields["job_functions"].choices = [
            (job_function.code, job_function.name)
            for job_function in JobFunction.objects.all()
        ]


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = [
            "auto_archive",
            "archive_after_weeks",
        ]

        widgets = {"auto_archive": forms.CheckboxInput()}
