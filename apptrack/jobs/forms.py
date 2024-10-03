
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

    def save(self, *args, **kwargs):
        return super().save(commit=False)
    

    
