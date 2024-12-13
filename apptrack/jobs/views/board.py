
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET

from jobs.models import Job, Board
from jobs.forms import JobForm


@login_required
@require_GET
def board_view(request):

    # Retrieve context data
    jobs = Job.objects.filter(
        profile=request.user.profile, archived=False).all()
    board = Board.objects.get(profile=request.user.profile)
    columns = board.columns.all()
    job_form = JobForm()
    edit_forms = {job.id: JobForm(instance=job) for job in jobs}
    context = {
        'user_id': request.user.id,
        'board': board,
        'columns': columns,
        'jobs': jobs,
        'job_form': job_form,
        'edit_forms': edit_forms,
    }

    # Render template
    return render(request, 'jobs/jobs_kanban.html', context)