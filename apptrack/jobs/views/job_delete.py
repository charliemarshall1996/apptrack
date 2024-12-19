from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View

from jobs.models import Job


class JobDeleteView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = Job
    success_url = reverse_lazy("jobs:board")
    success_message = "Job deleted successfully"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        job = self.model.objects.get(id=kwargs["pk"])
        job.delete()
        return redirect(reverse("jobs:board"))
