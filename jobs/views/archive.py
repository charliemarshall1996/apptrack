"""Manages requests to archive jobs."""
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import View

from jobs.models import Job

logger = logging.getLogger(__name__)


class JobArchiveView(LoginRequiredMixin, View):
    """POST only view to archive jobs."""

    def post(self, request, *args, **kwargs):
        """Archives a job.

        This view takes a POST request to archive a job. The job_id is
        expected to be in the request.POST dictionary. The job is set to
        archived = True, and the view redirects to the jobs:board URL.

        Args:
            request (HttpRequest): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponseRedirect: The response object.
        """
        logger.debug("Archiving job...")
        job_id = request.POST.get("job_id")
        job = Job.objects.get(id=job_id)

        job.archived = True  # Assuming `is_archived` is a boolean field
        job.save()
        logger.debug("Job %s archived", job_id)
        return redirect("jobs:board")
