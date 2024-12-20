"""Views for the tasks app."""

from django.shortcuts import render

from .models import Task


def task_cards_view(request):
    """View for the task cards page."""
    tasks = Task.objects.filter(
        profile=request.user.profile, is_completed=False
    ).order_by("priority")
    return render(
        request, "tasks/task_cards.html", {"tasks": tasks, "user_id": request.user.id}
    )
