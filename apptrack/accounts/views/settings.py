import logging

from django.contrib import messages
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile, Target
from accounts.forms import UserUpdateForm, ProfileUpdateForm, TargetUpdateForm
from accounts.messages import AccountsMessageManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
User = get_user_model()


@login_required
def settings_view(request, id):
    # Fetch the profile using the slug
    profile = get_object_or_404(Profile, id=id)
    target = get_object_or_404(Target, profile=profile)

    # Check if the logged-in user owns the profile, otherwise redirect
    if profile.user != request.user:
        messages.error(
            request, "You are not authorized to view or edit this profile.")
        return redirect('core:home')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        target_form = TargetUpdateForm(request.POST, instance=target)

        if user_form.is_valid() and profile_form.is_valid() and target_form.is_valid():

            user = user_form.save()
            user.save()
            target = target_form.save()
            target.save()
            profile = profile_form.save()
            profile.user = user
            profile.target = target
            profile.save()

            messages.success(
                request, AccountsMessageManager.profile_update_success)

            return redirect('accounts:profile', id=profile.id)
        else:
            if not profile_form.is_valid():
                errors = profile_form.errors.as_data()
                if errors.get('birth_date'):
                    messages.error(
                        request, AccountsMessageManager.invalid_birth_date)

            messages.error(
                request, f"Invalid form {profile_form.errors} {user_form.errors} {target_form.errors}")
            return redirect("accounts:profile", id=profile.id)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        target, created = Target.objects.get_or_create(profile=profile)
        target_form = TargetUpdateForm(instance=target)

    context = {
        'user_id': request.user.id,
        'target_form': target_form,
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    }
    return render(request, 'accounts/profile_settings.html', context)
