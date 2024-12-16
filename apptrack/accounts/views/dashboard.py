
from django.shortcuts import render
from django.utils import timezone

from jobs.models import Job, Interview, Task


def dashboard_view(request):
    jobs = Job.objects.filter(
        profile=request.user.profile, archived=False).order_by("updated").all()[:10]
    interviews = Interview.objects.filter(
        profile=request.user.profile, start_date__gte=timezone.now()).order_by("start_date").all()[:10]
    tasks = Task.objects.filter(
        profile=request.user.profile, is_completed=False).order_by("priority").all()[:10]

    context = {"user_id": request.user.id, "jobs": jobs,
               "interviews": interviews, "tasks": tasks}
    return render(request, "accounts/dashboard.html", context)
