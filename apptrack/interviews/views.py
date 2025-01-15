import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Interview
from accounts.models import Profile
from jobs.forms import AddInterviewForm, AddReminderForm
# Create your views here.

User = get_user_model()


def home_view(request):
    pass


@login_required
@require_GET
def calendar_view(request):
    # Prepare get data
    """Displays a calendar for the requesting user's interviews.

    The calendar displays each interview with its title, start and end times,
    and id. The user can add new interviews and reminders, edit existing ones,
    and view all their associated reminders.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: Redirects to the calendar view.
    """
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


class API(APIView):

    def get(self, request):
        user = User(id=request.user.id)
        profile = Profile(user=user)
        data = {
            "success": True,
            "interviews": self._get_interviews(profile),

        }
        return Response(data)

    def _get_interviews(self, profile):
        all_interviews = []
        interview_objects = Interview.objects.filter(profile=profile)

        for interview in interview_objects:
            interview_tasks = [
                {"id": task.id, "name": task.name, "completed": task.is_completed}
                for task in interview.tasks.all()
            ]
            all_interviews.append({
                "id": interview.id,
                "title": interview.job.job_title,
                "company": interview.job.company,
                # Just the date part (YYYY-MM-DD)
                "date": interview.start_date.date().isoformat(),
                # Start time (HH:MM)
                "start_time": interview.start_date.strftime("%H:%M"),
                # End time (HH:MM)
                "end_time": interview.end_date.strftime("%H:%M"),
                "notes": interview.notes,
                "tasks": interview_tasks
            })
        return all_interviews

    def post(self, request):
        pass
