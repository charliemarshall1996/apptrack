from django.shortcuts import render
from django.utils import timezone

from jobs.models import Job


def dashboard_view(request):
    """A view that renders a dashboard for the user.

    This view renders the dashboard template with the following data:

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
        .all()[:5]
    )

    context = {
        "user_id": request.user.id,
        "jobs": jobs
    }
    return render(request, "accounts/dashboard.html", context)
