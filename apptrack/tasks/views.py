from django.shortcuts import render

from .models import Task


def task_cards_view(request):
    tasks = Task.objects.filter(
        profile=request.user.profile, is_completed=False
    ).order_by("priority")
    return render(
        request, "tasks/task_cards.html", {"tasks": tasks, "user_id": request.user.id}
    )
