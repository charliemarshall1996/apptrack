"""Manages the editing of interviews for the requesting user."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from jobs.forms import AddInterviewForm


@login_required
@require_POST
def interview_edit_view(request):
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

    return redirect("interview:calendar")
