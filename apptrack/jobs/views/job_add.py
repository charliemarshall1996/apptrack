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
    logger.info("Adding job...")
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
