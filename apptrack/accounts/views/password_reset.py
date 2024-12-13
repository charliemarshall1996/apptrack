
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from accounts.forms import PasswordResetForm
from accounts.mail import AccountsEmailManager
from accounts.messages import AccountsMessageManager

User = get_user_model()

email_manager = AccountsEmailManager()


def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():

            if form.cleaned_data['honeypot']:
                messages.error(
                    request, AccountsMessageManager.spam)
                return redirect('core:home')

            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                email_manager.mail_password_reset(request, user)
                messages.success(
                    request, AccountsMessageManager.password_reset_success)
                return redirect("accounts:password_reset")
            else:
                messages.error(
                    request, AccountsMessageManager.email_not_found)
            return redirect('accounts:password_reset')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})
