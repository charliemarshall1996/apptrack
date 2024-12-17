
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import Profile

from .forms import TargetUpdateForm
from .models import Target
# Create your views here.


@login_required
def target_update_view(request):
    if request.method == "GET":
        target = Target.objects.get(user=request.user)
        form = TargetUpdateForm(instance=target)
        return render(request, 'target/target_update.html', {'form': form})

    if request.method == "POST":
        target = Target.objects.get(user=request.user)
        form = TargetUpdateForm(request.POST, instance=target)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Target updated successfully")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Target update failed")
            return redirect('accounts:dashboard')
