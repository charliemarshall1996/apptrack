
import csv
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy

from .forms import JobForm, DownloadJobsForm
from .models import Job, Board, Column

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
    try:
        board = Board.objects.get(user=request.user)
    except MultipleObjectsReturned:
        board = Board.objects.filter(user=request.user).first()

    if not board:
        # Handle case if the user doesn't have a board yet (optional)
        return HttpResponse("Board not found", status=404)

    # Check if required columns exist in the board
    for column_name, column_position in default_columns:

        try:
            column, created = Column.objects.get_or_create(
                name=column_name, board=board, position=column_position)

            # If the column was just created, add it to the board
            if created:
                column.save()
                print(f"Created and added missing column: {column_name}")

        except MultipleObjectsReturned:
            # Handle case if multiple columns
            # with the same name exist
            column = Column.objects.filter(
                name=column_name, board=board, position=column_position).first()

    # Retrieve jobs and columns for the user
    jobs = Job.objects.filter(user=request.user).all()
    columns = board.columns.all()
    job_form = JobForm()

    # Handle form submissions
    if request.method == "POST":
        job_form = JobForm(request.POST)

        if job_form.is_valid():
            job = job_form.save()
            job.board = board
            job.user = request.user
            job.save()

    # Context for rendering the template
    context = {
        'board': board,
        'columns': columns,
        'jobs': jobs,
        'job_form': job_form,
    }

    return render(request, 'jobs/jobs_kanban.html', context)


@login_required
def add_job_view(request):
    board = Board.objects.filter(user=request.user).first()
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
        return render(request, 'jobs/jobs_kanban.html')

    @staticmethod
    def post(request, *args, **kwargs):
        col_id = kwargs['col_id']
        job_id = kwargs['job_id']
        print(f"col_id: {col_id}, job_id: {job_id}")
        column = Column.objects.get(id=col_id)
        job = Job.objects.get(id=job_id)
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

    model = Job
    success_url = reverse_lazy('jobs:board')
    success_message = 'Job deleted successfully'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        job = self.model.objects.get(id=kwargs["pk"])
        job.delete()
        return redirect(reverse("jobs:board"))


class EditJobView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Job
    template_name = "jobs/edit_job.html"
    success_url = reverse_lazy("jobs:board")
    success_message = "Job updated successfully"
    fields = ['job_title', 'job_function', 'url', 'description', 'company',
              'location_policy', 'min_pay', 'max_pay', 'pay_rate', 'currency',  'note']


@login_required
def download_jobs_view(request):
    # Handle GET request (date input form rendering)
    if request.method == "GET":
        form = DownloadJobsForm()
        return render(request, "jobs/download_jobs.html", {"form": form})

    # Handle POST request (CSV file generation)
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    # Filter jobs based on the `updated` field
    jobs = Job.objects.filter(updated__range=(
        start_date, end_date)).order_by("id")

    filename = f"jobs_{start_date}_{end_date}.csv"
    # Prepare the response
    response = HttpResponse(
        content_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})

    # Write the CSV file
    writer = csv.writer(response)
    writer.writerow(["ID", "Job Title", "Company", "URL",
                    "Status", "Updated"])  # CSV headers

    for job in jobs:
        writer.writerow([job.id, job.job_title, job.company,
                        job.url, job.get_status_display(), job.updated])

    return response
