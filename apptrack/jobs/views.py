import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from core.forms import LocationForm

from .forms import JobForm, CompanyForm, UserJobsDetailsForm
from .models import Jobs, Companies, UserJobsDetails

logger = logging.getLogger(__name__)

# Create your views here.
class JobsListView(ListView):
    model = UserJobsDetails
    template_name = "jobs/jobs_list.html"
    context_object_name = "jobs"
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the status from the query parameters
        status_filter = self.request.GET.get('status', 'all')
        if status_filter == 'open':
            queryset = queryset.filter(status='open')
        elif status_filter == 'applied':
            queryset = queryset.filter(status='applied')
        elif status_filter == 'shortlisted':
            queryset = queryset.filter(status='shortlisted')
        elif status_filter == 'interview':
            queryset = queryset.filter(status='interview')
        elif status_filter == 'offer':
            queryset = queryset.filter(status='offer')
        elif status_filter == 'rejected':
            queryset = queryset.filter(status='rejected')
        elif status_filter == 'closed':
            queryset = queryset.filter(status='closed')
        else:
            queryset = queryset.filter(status='open')

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
        user_job_details_form = UserJobsDetailsForm(request.POST)

        # Check if all forms are valid
        if user_job_details_form.is_valid():
            user_job_details = user_job_details_form.save()
            user_job_details.user = request.user
            user_job_details.save()
            return redirect('jobs_list')
    else:
        user_job_details_form = UserJobsDetailsForm()

    return render(request, 'jobs/add_job.html', {
        'user_jobs_form': UserJobsDetailsForm()
    })