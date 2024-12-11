
import json
import csv
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import View, ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy

from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import (JobForm,
                    DownloadJobsForm,
                    JobFilterForm,
                    AddInterviewForm,
                    AddReminderForm)
from .models import (Job,
                     Board,
                     Column,
                     Interview,
                     InterviewTask,
                     InterviewReminder)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create your views here.


class ArchiveJobView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, *args, **kwargs):
        print("Archiving job...")
        job_id = request.POST.get('job_id')
        job = Job.objects.get(id=job_id)

        job.archived = True  # Assuming `is_archived` is a boolean field
        job.save()

        return redirect('jobs:board')


@login_required
def board_view(request):
    board = Board.objects.get(profile=request.user.profile)

    # Retrieve jobs and columns for the user
    jobs = Job.objects.filter(
        profile=request.user.profile, archived=False).all()
    columns = board.columns.all()
    job_form = JobForm()
    edit_forms = {job.id: JobForm(instance=job) for job in jobs}
    # Handle form submissions
    if request.method == "POST":
        job_form = JobForm(request.POST)

        if job_form.is_valid():
            job = job_form.save()
            job.board = board
            job.profile = request.user.profile
            job.save()
            messages.success(request, "Job added successfully")
            return redirect('jobs:board')

    # Clear session variables after passing them to the template
    for form in edit_forms.values():
        for field in form.fields:
            print(f"Filed: {field}, Type: {type(field)}")
    context = {
        'user_id': request.user.id,
        'board': board,
        'columns': columns,
        'jobs': jobs,
        'job_form': job_form,
        'edit_forms': edit_forms,
    }

    return render(request, 'jobs/jobs_kanban.html', context)


@login_required
@require_POST
def add_job_view(request):
    logger.info("Adding job...")
    board = Board.objects.filter(profile=request.user.profile).first()
    referer_url = request.POST.get("referrer")
    print("Referer URL: %s", referer_url)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            job.board = board
            job.profile = request.user.profile
            job.save()
            return redirect(referer_url)


@login_required
@require_POST
def edit_job_view(request, pk):
    logger.info("Editing job...")
    job = Job.objects.get(pk=pk)
    referer_url = request.POST.get("editJobReferrer")
    logger.info("Referer URL: %s", referer_url)
    if request.method == 'POST':
        logger.info("Request method is POST")
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            logger.info("Form is valid")
            job = form.save()
            job.save()
            logger.info("Job saved")
            logger.info("New job url: %s", job.url)
            return redirect(referer_url)


class AssignJobView(APIView):

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
        data = {"job_status": job.status, "job_id": job.id}
        return Response(data)


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
        print(obj)
        return obj


@login_required
def download_jobs_view(request):
    # Handle GET request (date input form rendering)
    if request.method == "GET":
        form = DownloadJobsForm()
        return render(request, "jobs/download_jobs.html", {"form": form, "user_id": request.user.id})

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
    ordering = ['-updated']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile=self.request.user.profile)
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
            archived = form.cleaned_data.get('archived')
            if archived != 'in':
                if archived == 'on':
                    queryset = queryset.filter(archived=True)
                else:
                    queryset = queryset.exclude(archived=True)

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


# Create your views here.


@login_required
def calendar(request):

    if request.method == "POST":
        print("form is post")
        print(f"request body {request.body}")
        print(f"request post {str(request.POST)}")
        print(f"request headers {request.headers}")
        body = json.loads(request.body)
        form_type = request.POST.get('form_type')
        if not form_type:
            form_type = body['form_type']
        if form_type == "add":
            form = AddInterviewForm(request.POST)
            if form.is_valid():
                interview = form.save()
                interview.profile = request.user.profile
                interview.save()
        elif form_type == "add_task":
            pass
        elif form_type == "update_task":
            print("update task")
            task_id = body["task_id"]
            task = InterviewTask.objects.get(id=task_id)
            task.is_completed = body["completed"]
            task.save()
            print(
                f"Task updated: {task.name} - Completed: {task.is_completed}")
        elif form_type == "delete_task":
            pass
        else:
            print(f"invalid form type {form_type}")

    add_form = AddInterviewForm()

    add_reminder_form = AddReminderForm()
    # Handle GET requests or invalid POST submissions
    all_interviews = Interview.objects.filter(profile=request.user.profile)
    interviews = []
    for interview in all_interviews:
        interview_data = {
            'title': f"{interview.job.job_title} at {interview.job.company}",
            'start': interview.start_date.isoformat(),
            'end': interview.end_date.isoformat(),
            'id': interview.id
        }
        interviews.append(interview_data)

    edit_forms = {i.id: AddInterviewForm(instance=i) for i in all_interviews}

    context = {
        "user_id": request.user.id,
        "add_form": add_form,
        "add_reminder_form": add_reminder_form,
        "interviews": json.dumps(interviews),
        "all_interviews": all_interviews,
        "edit_forms": edit_forms
    }
    return render(request, 'interview/calendar.html', context)


@login_required
@require_POST
def add_interview(request):
    print(f"request {request}")
    if request.method == "POST":
        form = AddInterviewForm(request.POST)
        if form.is_valid():
            interview = form.save()

            # Get the Reminders JSON string from the POST data
            # Use 'Reminders' as the key, as it's the name of the hidden input field
            reminders_json = request.POST.get('reminders')

            # Parse the JSON string back into a Python list (or another appropriate type)
            if reminders_json:
                reminders = json.loads(reminders_json)
                for r in reminders:
                    InterviewReminder.objects.create(
                        interview=interview,
                        offset=r['offset'],
                        unit=r['unit']
                    )
            else:
                reminders = []

            # Save the interview data and associated reminders
            interview.profile = request.user.profile
            interview.save()

            return redirect("interview:calendar")


@login_required
@require_POST
def edit_interview(request):
    if request.method == "POST":
        form = AddInterviewForm(request.POST)
        if form.is_valid():
            interview = form.save()
            interview.save()
            messages.success(request, "Interview updated successfully")
            return redirect("interview:calendar")


def interview_event_detail(request, interview_id):
    try:
        interview = Interview.objects.get(id=interview_id)
        print(interview.start_date.isoformat())

        interview_reminders = [
            {'id': r.id, 'offset': r.offset, 'unit': r.unit} for r in interview.reminders.all()
        ]

        interview_tasks = [{'id': task.id, 'name': task.name, 'completed': task.is_completed}
                           for task in interview.tasks.all()]
        # Return interview data as JSON
        response_data = {
            'id': interview.id,
            'title': interview.job.job_title,
            'company': interview.job.company,
            # Just the date part (YYYY-MM-DD)
            'date': interview.start_date.date().isoformat(),
            # Start time (HH:MM)
            'start_time': interview.start_date.strftime('%H:%M'),
            # End time (HH:MM)
            'end_time': interview.end_date.strftime('%H:%M'),
            'notes': interview.notes,
            'tasks': interview_tasks,
            'reminders': interview_reminders
        }
        print(response_data)
        return JsonResponse(response_data)
    except Interview.DoesNotExist:
        return JsonResponse({'error': 'Interview not found'}, status=404)


@login_required
@require_POST
def update_task(request, id):
    if request.method == "POST":
        task = InterviewTask.objects.get(id=id)
        is_completed = json.loads(request.body)['completed']
        if is_completed == "true":
            task.is_completed = True
        else:
            task.is_completed = False
        task.save()
        return HttpResponse(status=200)
