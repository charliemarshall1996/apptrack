
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

# Create your views here.
from .models import Task


def task_cards_view(request):
    tasks = Task.objects.filter(
        profile=request.user.profile, is_completed=False).order_by('priority')
    return render(request, 'tasks/task_cards.html', {'tasks': tasks, 'user_id': request.user.id})


@login_required
@require_POST
def task_update_view(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        is_completed = json.loads(request.body)['completed']
        if is_completed == "true":
            task.is_completed = True
        else:
            task.is_completed = False
        task.save()
        return HttpResponse(status=200)
