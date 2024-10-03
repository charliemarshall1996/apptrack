import logging
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse
from core.forms import LocationForm

from .forms import JobForm
from .models import Jobs

logger = logging.getLogger(__name__)

# Create your views here.
class JobsListView(ListView):
    model = Jobs
    template_name = "jobs/jobs_list.html"
    context_object_name = "jobs"
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(user=self.request.user)
        # Get the status from the query parameters
        status_filter = self.request.GET.get('status', 'all')
        if status_filter == 'OP':
            queryset = queryset.filter(status='OP')
        elif status_filter == 'AP':
            queryset = queryset.filter(status='AP')
        elif status_filter == 'SL':
            queryset = queryset.filter(status='SL')
        elif status_filter == 'IN':
            queryset = queryset.filter(status='IN')
        elif status_filter == 'OF':
            queryset = queryset.filter(status='OF')
        elif status_filter == 'RE':
            queryset = queryset.filter(status='RE')
        elif status_filter == 'CL':
            queryset = queryset.filter(status='CL')
        else:
            queryset = queryset.filter(status='OP')

        return queryset
    
def job_detail(request, job_id):
    job = get_object_or_404(Jobs, id=job_id)
    location = job.location  # Access the related location object

    context = {
        'job': job,
        'location': location,
        'country': location.get_country_display(),
        'region': location.region,
        'city': location.city,
    }

    return render(request, 'job_detail.html', context)
    

def add_job_view(request):
    if request.method == 'POST':
        job_form = JobForm(request.POST)
        location_form = LocationForm(request.POST)

        if job_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            location.save()
            job = job_form.save()
            job.location = location
            job.user = request.user
            job.save()
            return redirect('jobs_list')

    else:
        location_form = LocationForm()
        job_form = JobForm()

    return render(request, 'jobs/add_job.html', {'job_form': job_form, 'location_form': location_form})