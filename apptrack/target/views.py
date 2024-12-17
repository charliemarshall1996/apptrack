
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.dispatch import Signal
from django.shortcuts import redirect, render
from django.utils import timezone

from accounts.models import Profile

from .forms import TargetUpdateForm
from .models import Target
# Create your views here.

target_reset = Signal()


@login_required
def target_update_view(request):
    target = Target.objects.get(profile=request.user.profile)
    if request.method == "GET":

        form = TargetUpdateForm(instance=target)
        return render(request, 'target/target_update.html', {'form': form, 'user_id': request.user.id})

    if request.method == "POST":
        form = TargetUpdateForm(request.POST, instance=target)
        if form.is_valid():
            target = form.save()
            target.current = 0
            target.last_reset = timezone.now()
            target.save()
            target_reset.send(sender=target.__class__, instance=Target.objects.get(
                profile=request.user.profile))

            print(f"Target updated for user: {request.user.id}")
            print(f"Target amount: {target.amount}")
            messages.success(request, "Target updated successfully")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Target update failed")
            return redirect('accounts:dashboard')
