"""Manages the adding of jobs for the requesting user."""
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from jobs.forms import JobForm

logger = logging.getLogger(__name__)


@login_required
@require_POST
def job_add_view(request):
    """Handles POST requests to add a new job for the requesting user.

    This view processes the submitted job form data. If the form is valid,
    it saves the job, associates it with the user's profile and board, and
    redirects to the referring URL. The referring URL is obtained from the
    request.POST dictionary, passed as a hidden input field on the add_job_modal.

    Args:
        request (HttpRequest): The request object containing form data.

    Returns:
        HttpResponseRedirect: Redirects to the referring URL. If the form is valid, the 
            response will contain a success message. If the form is invalid, the 
                response will contain an error message.
    """
    if request.method == "POST":
        form = JobForm(request.POST, profile=request.user.profile)

        if form.is_valid():
            job = form.save()
            job.profile = request.user.profile
            job.save()
            messages.success(request, "Job added successfully!")
        else:
            messages.error(request, f"Failed to add job {form.errors}. \
                           Please try again.")

    return redirect("jobs:list")
