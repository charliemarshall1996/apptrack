import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from jobs.models import Job
from jobs.forms import JobForm

logger = logging.getLogger(__name__)


@login_required
@require_POST
def job_edit_view(request, pk):
    logger.info("Editing job...")
    job = Job.objects.get(pk=pk)
    referer_url = request.POST.get("editJobReferrer")
    logger.info("Referer URL: %s", referer_url)
    if request.method == "POST":
        logger.info("Request method is POST")
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            logger.info("Form is valid")
            job = form.save()
            job.save()
            logger.info("Job saved")
            logger.info("New job url: %s", job.url)
            return redirect(referer_url)
