
from datetime import datetime

from django import forms

from .models import Jobs, Companies, UserJobsDetails

class UserJobsDetailsForm(forms.ModelForm):

    class Meta:
        model = UserJobsDetails
        fields = ['status', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        return super().save(commit=False)
    
class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ['job_title', 
                  'job_function', 
                  'description', 
                  'url', 
                  'source', 
                  'work_contract', 
                  'location_policy', 
                  'pay_rate', 
                  'min_pay', 
                  'max_pay', 
                  'currency']
        
    def save(self, *args, **kwargs):
        return super().save(commit=False)

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = ['name', 'website', 'linkedin', 'description', 'industry', 'is_recruiter']

    def __init__(self, *args, **kwargs):
        self.company_exists = None
        self.user = kwargs.pop('user', None)  # Pop the user argument from kwargs
        super().__init__(*args, **kwargs)

    def clean_name(self):
        # Normalize the company name
        name = self.cleaned_data.get('name')
        if name:
            name = name.lower().title().strip()

        # Check if the company already exists
        company = Companies.objects.filter(name=name).exclude(pk=self.instance.pk).first()
        
        self.company_exists = bool(company)

        return name


    def save(self):
        # The `clean_name` method ensures unique validation logic is applied correctly
        name = self.cleaned_data.get('name')

        # If the company already exists (self.instance is set in the form)
        if self.company_exists:
            company = Companies.objects.filter(name=name).first()
        else:
            company = self.instance

        # Set the 'created_by' field with the current user
        if self.user and not self.company_exists:
            company.created_by = self.user
        
        if self.user:
            company.updated_by = self.user

        # Update or create fields with the form data
        company.website = self.cleaned_data.get('website')
        company.linkedin = self.cleaned_data.get('linkedin')
        company.description = self.cleaned_data.get('description')
        company.industry = self.cleaned_data.get('industry')
        company.is_recruiter = self.cleaned_data.get('is_recruiter')

        # Update the 'updated_by' field with the current user
        if self.user:
            company.updated_by = self.user

        return company
    

    
