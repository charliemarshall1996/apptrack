
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect

from accounts.messages import AccountsMessageManager


def verify_email_view(request, user_id, token):
    from accounts.tokens import email_verification_token  # Import the token generator
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, id=user_id)

    if email_verification_token.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(
            request, AccountsMessageManager.email_verified)
        return redirect('accounts:login')
