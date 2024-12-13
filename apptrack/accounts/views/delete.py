
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.messages import AccountsMessageManager


@ login_required
def delete_account_view(request):
    # Handle the POST request (when the user confirms the deletion)
    if request.method == 'POST':
        user = request.user  # Get the logged-in user
        user.profile.delete()  # Delete the user's profile
        user.delete()  # Delete the user account
        messages.success(
            request, AccountsMessageManager.account_deleted_success)
        return redirect('core:home')  # Redirect to the homepage after deletion

    # Render the confirmation page
    return render(request, 'accounts/delete_account.html')
