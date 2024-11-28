
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy

from core.forms import LocationForm
from .forms import JobForm
from .models import Jobs, Boards, Columns

logger = logging.getLogger(__name__)

# Create your views here.


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

        try:
            column, created = Columns.objects.get_or_create(
                name=column_name, board=board, position=column_position)

            # If the column was just created, add it to the board
            if created:
                column.save()
                print(f"Created and added missing column: {column_name}")

        except MultipleObjectsReturned:
            # Handle case if multiple columns
            # with the same name exist
            column = Columns.objects.filter(
                name=column_name, board=board, position=column_position).first()

    # Retrieve jobs and columns for the user
    jobs = Jobs.objects.filter(user=request.user).all()
    columns = board.columns.all()
    job_form = JobForm()
    location_form = LocationForm()

    # Handle form submissions (this section depends on whether you're submitting via POST)
    if request.method == "POST":
        job_form = JobForm(request.POST)
        location_form = LocationForm(request.POST)

        if job_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            job = job_form.save()
            job.board = board
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
    board = Boards.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            job.board = board
            job.user = request.user
            job.save()
            return redirect('jobs:board')
    else:
        form = JobForm()

    context = {
        'job_form': form
    }
    return render(request, 'jobs/jobs_kanban.html', context)


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
