import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET

from jobs.forms import AddInterviewForm, AddReminderForm
from jobs.models import Interview


@login_required
@require_GET
def calendar_view(request):
    # Prepare get data
    add_form = AddInterviewForm()
    add_reminder_form = AddReminderForm()
    all_interviews = Interview.objects.filter(profile=request.user.profile)
    interviews = []

    for interview in all_interviews:
        interview_data = {
            "title": f"{interview.job.job_title} at {interview.job.company}",
            "start": interview.start_date.isoformat(),
            "end": interview.end_date.isoformat(),
            "id": interview.id,
        }
        interviews.append(interview_data)
    edit_forms = {i.id: AddInterviewForm(instance=i) for i in all_interviews}

    context = {
        "user_id": request.user.id,
        "add_form": add_form,
        "add_reminder_form": add_reminder_form,
        "interviews": json.dumps(interviews),
        "all_interviews": all_interviews,
        "edit_forms": edit_forms,
    }
    return render(request, "jobs/calendar.html", context)
