
import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class EmailManager:

    sender = settings.DEFAULT_FROM_EMAIL

    def send(self, subject, message, html_message, recipient_list):
        logger.info("Sending email to %s", recipient_list)
        send_mail(subject, message, self.sender,
                  recipient_list, html_message=html_message)
