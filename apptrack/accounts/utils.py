
from datetime import timedelta

from django.utils import timezone


def get_time_since_last_email(last_email_sent):
    return timezone.now() - last_email_sent


def get_can_resend(timeout_duration, time_since_last_email):
    return time_since_last_email > timeout_duration


def get_minutes_left_before_resend(time_since_last_email, timeout_duration):
    time_difference = timeout_duration - time_since_last_email
    total_seconds = time_difference.total_seconds()
    return total_seconds // 60


class MessageManager:
    password_reset_success = """We've emailed you instructions for setting your password, 
        if an account exists with the email you entered. You should receive them 
        shortly. If you don't receive an email, please make sure you've entered the 
        address you registered with, and check your spam folder."""
    spam = "Your form submission was detected as spam."

    user_not_found = "We can't find a user with that email address."

    verification_email_sent = "Verification email sent. Please check your inbox."

    account_deleted_success = "Your account has been successfully deleted."

    profile_update_success = 'Your profile has been updated!'
