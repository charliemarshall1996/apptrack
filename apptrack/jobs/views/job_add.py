"""Manages the adding of jobs for the requesting user."""
import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from jobs.models import Board
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
        HttpResponseRedirect: Redirects to the referring URL if the form is valid.
    """
    logger.debug("Adding job...")
    board = Board.objects.filter(profile=request.user.profile).first()
    referer_url = request.POST.get("referrer")
    logger.debug("Referer URL: %s", referer_url)
    if request.method == "POST":
        logger.debug("Request method is POST")
        form = JobForm(request.POST)
        if form.is_valid():
            logger.debug("Form is valid")
            job = form.save()
            job.board = board
            job.profile = request.user.profile
            job.save()
            logger.debug("Job saved")
            return redirect(referer_url)
        else:
            logger.debug("Form is not valid %s", form.errors)
