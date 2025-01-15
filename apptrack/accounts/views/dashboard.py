from django.shortcuts import render
from django.utils import timezone

from jobs.models import Job
from interviews.models import Interview
from tasks.models import Task


def dashboard_view(request):
    """
    A view that renders a dashboard for the user
    with the following data:

    - The 10 most recently updated jobs
    - The 10 most recently scheduled interviews
    - The 10 tasks with the highest priority

    All data is associated with the user making
    the request.

    Args:
        - request: The current request

    Returns:
        - The rendered dashboard template
    """
    jobs = (
        Job.objects.filter(profile=request.user.profile, archived=False)
        .order_by("updated")
        .all()[:10]
    )
    interviews = (
        Interview.objects.filter(
            profile=request.user.profile, start_date__gte=timezone.now()
        )
        .order_by("start_date")
        .all()[:10]
    )
    tasks = (
        Task.objects.filter(profile=request.user.profile, is_completed=False)
        .order_by("priority")
        .all()[:10]
    )

    context = {
        "user_id": request.user.id,
        "jobs": jobs,
        "interviews": interviews,
        "tasks": tasks,
    }
    return render(request, "accounts/dashboard.html", context)
