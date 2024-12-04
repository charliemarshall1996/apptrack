
from django.core.mail import send_mail


class EmailManager:

    def __init__(self, user):
        self.user = user

    def send(self, email):
        pass
