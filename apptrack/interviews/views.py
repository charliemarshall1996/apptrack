
import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from .models import Interview
from .forms import AddInterviewForm

# Create your views here.

User = get_user_model()


@login_required
@require_GET
def home_view(request):
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
        "interviews": json.dumps(interviews),
        "all_interviews": all_interviews,
        "edit_forms": edit_forms,
    }
    return render(request, "interviews/home.html", context)


@login_required
@require_POST
def add_view(request):
    """Manages POST requests for the interview add view.

    If the request method is POST, it validates the form and saves the changes.
    If also handles associated reminders for the added interview, saving them.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: The response object.
    """
    form = AddInterviewForm(request.POST)
    if form.is_valid():
        interview = form.save()

        interview.profile = request.user.profile
        interview.save()

        messages.success(request, "Interview added successfully")
    else:
        messages.error(
            request, "Error adding interview: {}".format(form.errors))
    return redirect("interview:add")


@login_required
@require_POST
def edit_view(request):
    """Manages the editing of interviews for the requesting user.

    If the request method is POST, it validates the form and saves the changes.
    If the form is valid, it saves the interview and redirects to the interview
    calendar. If the form is invalid, the response will contain an error message.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: Redirects to the interview calendar.
    """
    form = AddInterviewForm(request.POST)

    if form.is_valid():
        interview = form.save()
        interview.save()
        messages.success(request, "Interview updated successfully")
    else:
        messages.error(request, f"Error updating interview: {form.errors}")

    return redirect("interview:home")


def detail_view(request, interview_id):
    """Provides the details of an interview as JSON.

    Args:
        request: The request object.
        interview_id: The ID of the interview to retrieve.

    Returns:
        A JSON response containing the interview details if the interview is found,
        otherwise a 404 response with an error message.
    """
    try:
        interview = Interview.objects.get(id=interview_id)
        print(interview.start_date.isoformat())

        interview_reminders = [
            {"id": r.id, "offset": r.offset, "unit": r.unit}
            for r in interview.reminders.all()
        ]

        interview_tasks = [
            {"id": task.id, "name": task.name, "completed": task.is_completed}
            for task in interview.tasks.all()
        ]
        # Return interview data as JSON
        response_data = {
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
            "tasks": interview_tasks,
            "reminders": interview_reminders,
        }
        print(response_data)
        return JsonResponse(response_data)
    except Interview.DoesNotExist:
        return JsonResponse({"error": "Interview not found"}, status=404)


"""class API(APIView):

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
        data = json.loads(request.body)
        print("data: ", data)
        post_type = data.get("post_type")

        if post_type == "add":
            self._add(data)
        elif post_type == "edit":
            self._edit(data)
        else:
            pass

    def _edit(self, data):
        pk = data.get("pk")

        interview = Interview.objects.get(pk=pk)
        pass

    def _add(self, data):
        pass"""
