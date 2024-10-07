
import logging
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import ListView, View
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from core.forms import LocationForm
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from .forms import JobForm
from .models import Jobs, Boards, Columns, Employee, Task

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


@login_required
def update_job_view(request, pk):
    job_to_update = Jobs.objects.get(pk=pk)

    if request.method == 'POST':
        job_form = JobForm(request.POST, instance=job_to_update)
        location_form = LocationForm(
            request.POST, instance=job_to_update.location)
        if job_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            location.save()
            job = job_form.save()
            job.location = location
            job.user = request.user
            job.save()
            messages.success(request, 'Your profile has been updated!')
            # Redirect to the profile page after saving
            return redirect('jobs_list')
    else:
        job_form = JobForm(instance=job_to_update)
        location_form = LocationForm(instance=job_to_update.location)

    context = {
        'job_form': job_form,
        'location_form': location_form
    }
    return render(request, 'jobs/update_job.html', context)


@login_required
def board_view(request):
    board = Boards.objects.filter(user=request.user).first()
    job_form = JobForm()
    location_form = LocationForm()

    if not board:
        return HttpResponse('No board available for this user.')

    if request.method == 'POST':
        job_form = JobForm(request.POST)
        location_form = LocationForm(request.POST)

        if job_form.is_valid() and location_form.is_valid():
            loc = location_form.save()
            new_job = job_form.save()
            new_job.location = loc
            new_job.user = request.user
            new_job.save()

            # Option 1: Redirect for a full refresh (existing behavior)
            if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return redirect('job_board')

    # Regular context for rendering the full page
    context = {
        'board': board,
        'job_form': job_form,
        'location_form': location_form,
    }

    return render(request, 'jobs/jobs_kanban.html', context)


@login_required
def assign_job_view(request):
    jobs = Jobs.objects.filter(user=request.user)
    columns = Columns.objects.all()
    context = {
        'jobs': jobs,
        'columns': columns
    }
    return render(request, 'jobs/partials/kanban_board.html')


# ...
class ChangeSheetAssign(LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        emp_id = kwargs['emp_id']
        task_id = kwargs['task_id']

        employee = Employee.objects.get(id=emp_id)
        task = Task.objects.get(id=task_id)

        employee.task = task
        task.save()

        return redirect(reverse('myapp:main_page'))

# render page


class AssignTaskView(LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        columns = Columns.objects.all()
        jobs = Jobs.objects.all()
        spare_jobs = Task.objects.filter(employee__isnull=True)

        context = {'columns': columns,
                   'jobs': jobs,
                   'spare_jobs': spare_jobs}

        return render(request, 'jobs/jobs_kanban.html', context)
