
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Interview, InterviewTask
from .forms import AddInterviewForm, AddReminderForm

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
                interview.user = request.user
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
    all_interviews = Interview.objects.filter(user=request.user)
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
    if request.method == "POST":
        form = AddInterviewForm(request.POST)
        if form.is_valid():
            interview = form.save()
            interview.user = request.user
            interview.save()
            return redirect("interview:calendar")


def interview_event_detail(request, interview_id):
    try:
        interview = Interview.objects.get(id=interview_id)
        print(interview.start_date.isoformat())

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
            'tasks': interview_tasks
        }
        print(response_data)
        return JsonResponse(response_data)
    except Interview.DoesNotExist:
        return JsonResponse({'error': 'Interview not found'}, status=404)
