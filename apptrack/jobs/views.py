
import csv
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import View, ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy

from .forms import JobForm, DownloadJobsForm, JobFilterForm
from .models import Job, Board, Column

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create your views here.


@login_required
def board_view(request):

    board = Board.objects.get(user=request.user)

    # Retrieve jobs and columns for the user
    jobs = Job.objects.filter(user=request.user).all()
    columns = board.columns.all()
    job_form = JobForm()
    edit_forms = {job.id: JobForm(instance=job) for job in jobs}
    # Handle form submissions
    if request.method == "POST":
        job_form = JobForm(request.POST)

        if job_form.is_valid():
            job = job_form.save()
            job.board = board
            job.user = request.user
            job.save()
            messages.success(request, "Job added successfully")
            return redirect('jobs:board')

    # Context for rendering the template
    context = {
        'user_id': request.user.id,
        'board': board,
        'columns': columns,
        'jobs': jobs,
        'job_form': job_form,
        'edit_forms': edit_forms
    }

    return render(request, 'jobs/jobs_kanban.html', context)


@login_required
@require_POST
def add_job_view(request):
    logger.info("Adding job...")
    board = Board.objects.filter(user=request.user).first()
    referer_url = request.POST.get("referrer")
    logger.info("Referer URL: %s", referer_url)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            job.board = board
            job.user = request.user
            job.save()
            return redirect(referer_url)


class AssignJobView(LoginRequiredMixin, View):

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

        return redirect('jobs:board')


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
    template_name = "jobs/jobs_kanban.html"
    success_url = reverse_lazy("jobs:board")
    success_message = "Job updated successfully"
    fields = ['job_title', 'job_function', 'url', 'description', 'company',
              'location_policy', 'min_pay', 'max_pay', 'pay_rate', 'currency',  'note']

    def get_object(self):
        # Custom logic to retrieve the object
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj


@login_required
def download_jobs_view(request):
    # Handle GET request (date input form rendering)
    if request.method == "GET":
        form = DownloadJobsForm()
        return render(request, "jobs/download_jobs.html", {"form": form, "user_id": request.user})

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


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        form = JobFilterForm(self.request.GET)

        if form.is_valid():
            statuses = form.cleaned_data.get('status')
            title = form.cleaned_data.get('title')
            job_functions = form.cleaned_data.get('job_function')
            company = form.cleaned_data.get('company')
            city = form.cleaned_data.get('city')
            region = form.cleaned_data.get('region')
            countries = form.cleaned_data.get('countries')
            location = form.cleaned_data.get('location')
            date_posted = form.cleaned_data.get('date_posted')

            if statuses:
                queryset = queryset.filter(status__in=statuses)
            if title:
                queryset = queryset.filter(job_title__icontains=title)
            if job_functions:
                queryset = queryset.filter(job_function__in=job_functions)
            if company:
                queryset = queryset.filter(company__icontains=company)
            if city:
                queryset = queryset.filter(city__icontains=city)
            if region:
                queryset = queryset.filter(region__icontains=region)
            if countries:
                queryset = queryset.filter(country__in=countries)

            if location:
                queryset = queryset.filter(location__icontains=location)
            if date_posted:
                queryset = queryset.filter(date_posted__gte=date_posted)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        context['filter_form'] = JobFilterForm(
            self.request.GET)  # Pass form to template
        context['job_form'] = JobForm()
        return context
