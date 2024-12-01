
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Interview
from .forms import AddInterviewForm

# Create your views here.


@login_required
def calendar(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == "add":
            form = AddInterviewForm(request.POST)
            if form.is_valid():
                interview = form.save()
                interview.user = request.user
                interview.save()

    add_form = AddInterviewForm()
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

    context = {
        "add_form": add_form,
        "interviews": json.dumps(interviews),
    }
    return render(request, 'interview/calendar.html', context)


@login_required
def add_interview(request):
    if request.method == "POST":
        form = AddInterviewForm(request.POST)
        if form.is_valid():
            interview = form.save()
            interview.user = request.user
            interview.save()
            return redirect("interview:calendar")
    else:
        form = AddInterviewForm()

    return render(request, "interview/calendar.html", {"form": form})

# views.py


def interview_detail(request, interview_id):
    try:
        interview = Interview.objects.get(id=interview_id)
        print(interview.start_date.isoformat())
        # Return interview data as JSON
        response_data = {
            'title': interview.job.job_title,
            # Just the date part (YYYY-MM-DD)
            'date': interview.start_date.date().isoformat(),
            # Start time (HH:MM)
            'start_time': interview.start_date.strftime('%H:%M'),
            # End time (HH:MM)
            'end_time': interview.end_date.strftime('%H:%M'),
            'notes': interview.notes,
        }
        return JsonResponse(response_data)
    except Interview.DoesNotExist:
        return JsonResponse({'error': 'Interview not found'}, status=404)
