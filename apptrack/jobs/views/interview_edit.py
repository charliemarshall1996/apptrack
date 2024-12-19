from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from jobs.forms import AddInterviewForm


@login_required
@require_POST
def interview_edit_view(request):
    if request.method == "POST":
        form = AddInterviewForm(request.POST)
        if form.is_valid():
            interview = form.save()
            interview.save()
            messages.success(request, "Interview updated successfully")
            return redirect("interview:calendar")
