
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from jobs.models import InterviewTask


@login_required
@require_POST
def task_edit_view(request, id):
    if request.method == "POST":
        task = InterviewTask.objects.get(id=id)
        is_completed = json.loads(request.body)['completed']
        if is_completed == "true":
            task.is_completed = True
        else:
            task.is_completed = False
        task.save()
        return HttpResponse(status=200)
