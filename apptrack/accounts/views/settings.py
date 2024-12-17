import logging

from django.contrib import messages
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from accounts.forms import UserUpdateForm, ProfileUpdateForm, TargetUpdateForm
from accounts.messages import AccountsMessageManager


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
User = get_user_model()


@login_required
def settings_view(request, id):
    # Fetch the profile using the slug
    profile = get_object_or_404(Profile, id=id)

    # Check if the logged-in user owns the profile, otherwise redirect
    if profile.user != request.user:
        messages.error(
            request, "You are not authorized to view or edit this profile.")
        return redirect('core:home')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.save()
            profile = profile_form.save()
            profile.user = user
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
                request, f"Invalid form {profile_form.errors} {user_form.errors}")
            return redirect("accounts:profile", id=profile.id)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_id': request.user.id,
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    }
    return render(request, 'accounts/profile_settings.html', context)
