
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
