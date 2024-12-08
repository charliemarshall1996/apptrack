
from typing import Any
from django import forms
from .models import Interview, InterviewTask, InterviewReminder


class AddInterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['job', 'start_date', 'end_date', 'post_code',
                  'building', 'street', 'town', 'region', 'country', 'notes']
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }

    def save(self) -> Any:
        return super().save(commit=False)


class AddReminderForm(forms.ModelForm):
    class Meta:
        model = InterviewReminder
        fields = ['offset', 'unit']


class TaskForm(forms.ModelForm):
    class Meta:
        model = InterviewTask
        fields = ['name', 'is_completed']
