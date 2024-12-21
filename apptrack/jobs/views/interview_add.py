"""Manages the interview add view for the requesting user."""
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from jobs.forms import AddInterviewForm
from jobs.models import InterviewReminder


@login_required
@require_POST
def interview_add_view(request):
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

        # Get the Reminders JSON string from the POST data
        # Use 'Reminders' as the key, as it's the name of the hidden input field
        reminders_json = request.POST.get("reminders")

        # Parse the JSON string back into a Python list (or another appropriate type)
        if reminders_json:
            reminders = json.loads(reminders_json)
            for r in reminders:
                InterviewReminder.objects.create(
                    interview=interview, offset=r["offset"], unit=r["unit"]
                )
        else:
            reminders = []

        interview.profile = request.user.profile
        interview.save()

        messages.success(request, "Interview added successfully")
    else:
        messages.error(
            request, "Error adding interview: {}".format(form.errors))
    return redirect("interview:calendar")
