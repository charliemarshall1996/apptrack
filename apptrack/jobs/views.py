
import logging
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import ListView, View
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from core.forms import LocationForm
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View

from .forms import JobForm
from .models import Jobs, Boards, Columns

logger = logging.getLogger(__name__)

# Create your views here.


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
    default_columns = [
        ('Open', 1),
        ('Applied', 2),
        ('Shortlisted', 3),
        ('Interview', 4),
        ('Offer', 5),
        ('Rejected', 6),
        ('Closed', 7),
    ]

    # Get the user's board or return 404 if not found
    board = Boards.objects.filter(user=request.user).first()

    if not board:
        # Handle case if the user doesn't have a board yet (optional)
        return HttpResponse("Board not found", status=404)

    # Check if required columns exist in the board
    for column_name, column_position in default_columns:
        column, created = Columns.objects.get_or_create(
            name=column_name, boards=board, position=column_position)

        # If the column was just created, add it to the board
        if created:
            board.columns.add(column)
            print(f"Created and added missing column: {column_name}")
        print(f"Column: {column}, created: {created}, jobs: {column.jobs}")

    # Retrieve jobs and columns for the user
    jobs = Jobs.objects.filter(user=request.user)
    columns = board.columns.all()
    job_form = JobForm()
    location_form = LocationForm()

    # Handle form submissions (this section depends on whether you're submitting via POST)
    if request.method == "POST":
        job_form = JobForm(request.POST)
        location_form = LocationForm(request.POST)

        if job_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            job = job_form.save(commit=False)  # Don't save job yet
            job.location = location
            job.user = request.user
            job.save()

    # Context for rendering the template
    context = {
        'board': board,
        'columns': columns,
        'jobs': jobs,
        'job_form': job_form,
        'location_form': location_form
    }

    return render(request, 'jobs/jobs_kanban.html', context)


@login_required
def add_job_view(request):
    referrer = request.META.get('HTTP_REFERER')

    print(f"user: {request.user}")

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

            if referrer:
                return HttpResponseRedirect(referrer)
            else:
                # Fallback to a default page if referrer is not available or unsafe
                return redirect(reverse('jobs:board'))
    else:
        job_form = JobForm()
        location_form = LocationForm()

    context = {
        'job_form': job_form,
        'location_form': location_form
    }
    return render(request, 'jobs/jobs_kanban.html', context)


class ChangeSheetAssign(LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        col_id = kwargs['col_id']
        job_id = kwargs['job_id']

        column = Columns.objects.get(id=col_id)
        job = Jobs.objects.get(id=job_id)

        job.column = column
        job.save()
        column.save()

        return redirect(reverse('jobs:board'))

# render page


class AssignJobView(LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        employees = Columns.objects.all()
        jobs = Jobs.objects.all()

        context = {'employees': employees,
                   'tasks': jobs}

        return render(request, 'jobs/jobs_kanban.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        col_id = kwargs['col_id']
        job_id = kwargs['job_id']
        print(f"col_id: {col_id}, job_id: {job_id}")
        column = Columns.objects.get(id=col_id)
        job = Jobs.objects.get(id=job_id)
        print(f"column: {column}, job: {job}")

        job.column = column

        try:
            job.save()
            column.save()
            print(f"Job assigned successfully to column: {column}")
        except Exception as e:
            print(f"Error: {e}")

        return redirect(reverse('jobs:board'))


class DeleteJobView(LoginRequiredMixin, SuccessMessageMixin, View):

    model = Jobs
    success_url = reverse_lazy('jobs:board')
    success_message = 'Job deleted successfully'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        job = self.model.objects.get(id=kwargs["pk"])
        job.delete()
        return redirect(reverse("jobs:board"))


class EditJobView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Jobs
    template_name = "jobs/edit_job.html"
    success_url = reverse_lazy("jobs:board")
    success_message = "Job updated successfully"
    fields = ['job_title', 'job_function', 'url', 'description', 'company_name',
              'location_policy', 'min_pay', 'max_pay', 'pay_rate', 'currency',  'note']


class JobsListView(LoginRequiredMixin, ListView):
    model = Jobs
    template_name = "jobs/jobs_list.html"
    context_object_name = "jobs"

    def get_queryset(self):
        jobs = Jobs.objects.filter(user=self.request.user)
        return jobs


@login_required
def jobs_list_view(request):
    jobs = Jobs.objects.filter(user=request.user)
    job_form = JobForm()
    location_form = LocationForm()
    if request.method == "POST":
        job_form = JobForm(request.POST)
        location_form = LocationForm(request.POST)

        if job_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            job = job_form.save(commit=False)  # Don't save job yet
            job.location = location
            job.user = request.user
            job.save()

    context = {
        'jobs': jobs,
        'job_form': job_form,
        'location_form': location_form
    }
    return render(request, 'jobs/jobs_list.html', context)
