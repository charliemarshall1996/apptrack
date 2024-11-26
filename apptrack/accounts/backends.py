from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailVerificationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        UserModel = get_user_model()
        try:
            # Authenticate using the email field
            user = UserModel.objects.get(email=email)
            if user.email_verified:
                if user.check_password(password):
                    print(f"User email verified: {user.email_verified}")
                    return user
            else:
                return None
        except UserModel.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """Override to add email verification logic."""
        is_active = super().user_can_authenticate(user)
        return is_active and user.email_verified
