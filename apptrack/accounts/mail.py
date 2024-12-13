
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.mail import EmailManager


class AccountsEmailManager(EmailManager):

    def __init__(self):
        super().__init__()

    def mail_verification(self, request, user):
        from .tokens import email_verification_token
        token = email_verification_token.make_token(user)
        verification_url = request.build_absolute_uri(
            reverse('accounts:verify_email', kwargs={
                    'user_id': user.id, 'token': token})
        )

        subject = "Verify your email"
        message = f"Please click the link to verify your email: {verification_url}"
        html_message = f"<p>Please click the link to verify your email: {verification_url}</p>"
        recipient = [user.email]
        self.send(subject, message, html_message, recipient)

    def mail_password_reset(self, request, user):
        from .tokens import password_reset_token
        token = password_reset_token.make_token(user)
        password_reset_url = request.build_absolute_uri(
            reverse('accounts:password_reset_confirm', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token})
        )

        subject = "Reset your password"
        message = f"Please click the link to reset your password: {password_reset_url}"
        html_message = f"<p>Please click the link to reset your password: {password_reset_url}</p>"
        recipient = [user.email]
        self.send(subject, message, html_message, recipient)
