import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from jobs.forms import AddInterviewForm
from jobs.models import InterviewReminder


@login_required
@require_POST
def interview_add_view(request):
    print(f"request {request}")
    if request.method == "POST":
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

            # Save the interview data and associated reminders
            interview.profile = request.user.profile
            interview.save()

            return redirect("interview:calendar")
