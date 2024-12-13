
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import View

from jobs.models import Job


class JobArchiveView(LoginRequiredMixin, View):

    def post(request, *args, **kwargs):
        print("Archiving job...")
        job_id = request.POST.get('job_id')
        job = Job.objects.get(id=job_id)

        job.archived = True  # Assuming `is_archived` is a boolean field
        job.save()

        return redirect('jobs:board')
