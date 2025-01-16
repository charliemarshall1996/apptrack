"""Manages the job delete view for the requesting user."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View

from jobs.models import Job


class JobDeleteView(LoginRequiredMixin, SuccessMessageMixin, View):
    """Manages the job delete view for the requesting user.

    If the request method is POST, it deletes the job and redirects to the job board.
    If the request method is GET, it redirects to the core home page.
    """
    model = Job
    success_url = reverse_lazy("jobs:board")
    success_message = "Job deleted successfully"

    def get(self, request, *args, **kwargs):  # noqa: D102
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # noqa: D102
        job = self.model.objects.get(id=kwargs["pk"])
        job.delete()
        return redirect(reverse("jobs:board"))
