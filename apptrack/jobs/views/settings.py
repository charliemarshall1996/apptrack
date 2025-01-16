
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from jobs.forms import SettingsForm
from jobs.models import Settings

User = get_user_model()


@login_required
def settings_view(request):
    pk = request.user.id

    user = User.objects.get(pk=request.user.pk)
    profile = user.profile
    if request.method == "GET":

        settings, created = Settings.objects.get_or_create(profile=profile)

        if created:
            settings.save()

        context = {
            "user_id": user.id,
            "form": SettingsForm(instance=settings)
        }

        return render(request, "jobs/settings.html", context)

    elif request.method == "POST":

        form = SettingsForm(request.POST, instance=profile.job_settings)

        if form.is_valid():
            form.save()
            messages.success(request, "Job settings saved successfully!")

        return redirect("jobs:settings")
