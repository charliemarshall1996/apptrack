"""Job edit view.

Manages the job edit view for the requesting user.
"""
import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from jobs.models import Job
from jobs.forms import JobForm

logger = logging.getLogger(__name__)


@login_required
@require_POST
def job_edit_view(request, pk):
    """Manages POST requests for the job edit view. GET requests are not supported.

    This view handles the editing of a job for the requesting user. If the request
    method is POST, it validates the form and saves the changes.

    Args:
        request (HttpRequest): The request object.
        pk (int): The primary key of the job to edit.

    Returns:
        HttpResponseRedirect: The response object.
    """
    logger.info("Editing job...")
    job = Job.objects.get(pk=pk)

    if request.method == "POST":
        logger.info("Request method is POST")
        form = JobForm(request.POST, instance=job,
                       profile=request.user.profile)
        if form.is_valid():
            logger.info("Form is valid")
            job = form.save()
            job.save()
            logger.info("Job saved")
            logger.info("New job url: %s", job.url)
            messages.success(request, "Job updated successfully!")
        else:
            logger.info("Form is not valid")
            messages.error(request, f"Error updating job: {form.errors}")

    return redirect("jobs:list")
