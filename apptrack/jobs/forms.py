from django import forms
from .models import Jobs

class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ['company', 'title', 'source', 'url', 'description', 'location', 'status', 'note']

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        url = cleaned_data.get('url')

        # Check if source is "web" and URL is empty
        if source == Jobs.WEB and not url:
            self.add_error('url', 'URL is required when the source is set to web.')

        return cleaned_data