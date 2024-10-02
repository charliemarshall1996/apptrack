from django import forms
from .models import Jobs, Company

class JobForm(forms.ModelForm):
    company_name = forms.CharField(max_length=255, required=False, label="Company Name (if new)")

    class Meta:
        model = Jobs
        fields = ['title', 'url', 'source', 'description', 'location', 'location_policy', 'status', 'work_contract', 'pay_rate', 'note', 'company_name']

    def clean(self):
        cleaned_data = super().clean()
        company_name = cleaned_data.get("company_name")
        company = cleaned_data.get("company")

        if not company and not company_name:
            raise forms.ValidationError("Please either select an existing company or provide a new company name.")

        return cleaned_data