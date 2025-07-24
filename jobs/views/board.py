"""Allows for a kanban-based view for the requesting user's jobs."""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.http import require_GET

from jobs.models import Job, Board
from jobs.forms import JobForm


@login_required
@require_GET
def board_view(request):
    # Retrieve context data
    """Retrieves context data for the requesting user's job board view.

    This view renders the jobs kanban template with the following context data:
        - The requesting user's ID
        - The requesting user's job board
        - The columns associated with the job board
        - The requesting user's jobs
        - A blank job form
        - A dictionary of job forms for each job, keyed by job ID

    If the job board does not exist for the requesting user, it creates a new
    job board and sends a warning message.
    """
    jobs = Job.objects.filter(
        profile=request.user.profile, archived=False).order_by('job_title',
                                                               'company').all()
    board, created = Board.objects.get_or_create(profile=request.user.profile)
    if created:
        messages.warning(
            request,
            "Job board was not found for your profile.\
                  A new job board has been created.",
        )
    columns = board.columns.all()
    job_form = JobForm()
    edit_forms = {job.id: JobForm(instance=job) for job in jobs}
    context = {
        "user_id": request.user.id,
        "board": board,
        "columns": columns,
        "jobs": jobs,
        "job_form": job_form,
        "edit_forms": edit_forms,
    }

    # Render template
    return render(request, "jobs/board.html", context)
