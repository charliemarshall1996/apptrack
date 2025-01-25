"""Views for the tasks app."""

from django.shortcuts import render
from rest_framework import (viewsets,
                            response,
                            renderers)
from rest_framework.decorators import action

from .models import Task
from .serializers import TaskSerializer


def task_cards_view(request):
    """View for the task cards page."""
    tasks = Task.objects.filter(
        profile=request.user.profile, is_completed=False
    ).order_by("priority")
    return render(
        request, "tasks/task_cards.html", {"tasks": tasks,
                                           "user_id": request.user.id}
    )


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile)

    def list(self, request):
        tasks = self.get_queryset()
        data = {"tasks": tasks}
        return response.Response(data, template_name="tasks/list.html")
