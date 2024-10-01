from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import JobForm
from .models import Jobs

# Create your views here.
class JobsListView(ListView):
    model = Jobs
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
    
def create_job_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jobs_list')
    else:
        form = JobForm()
    return render(request, 'jobs/create_job.html', {'form': form})