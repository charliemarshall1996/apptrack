
from django.shortcuts import render
from django.utils import timezone

from jobs.models import Job, Interview, Task


def home_view(request):
    jobs = Job.objects.filter(
        user=request.user, archived=False).order_by("updated").all()[:10]
    interviews = Interview.objects.filter(
        user=request.user, start_date__gte=timezone.now()).order_by("start_date").all()[:10]
    tasks = Task.objects.filter(
        user=request.user).order_by("priority").all()[:10]

    context = {"user_id": request.user.id, "jobs": jobs,
               "interviews": interviews, "tasks": tasks}
    return render(request, "accounts/dashboard.html", context)
