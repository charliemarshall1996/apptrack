
from datetime import datetime

from django import forms

from .models import Jobs


class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ['url',
                  'source',
                  'job_title',
                  'job_function',
                  'description',
                  'location_policy',
                  'work_contract',
                  'min_pay', 'max_pay',
                  'pay_rate', 'currency',
                  'note',
                  'status', 'company']

    def save(self, *args, **kwargs):
        return super().save(*args, commit=False, **kwargs)
