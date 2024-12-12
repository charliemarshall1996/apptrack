
from django.utils import timezone


def get_time_since_last_email(last_email_sent):
    return timezone.now() - last_email_sent


def get_can_resend(timeout_duration, time_since_last_email):
    return time_since_last_email > timeout_duration


def get_minutes_left_before_resend(time_since_last_email, timeout_duration):
    time_difference = timeout_duration - time_since_last_email
    total_seconds = time_difference.total_seconds()
    return total_seconds // 60


class ConversionCalculator:

    @staticmethod
    def calculate_basic_conversion_rate(applications, interviews_or_offers):
        if interviews_or_offers > 0 and applications > 0:
            return (interviews_or_offers / applications)
        else:
            return 0

    @staticmethod
    def calculate_conversion_rate(applications, interviews, offers):
        if interviews + offers > 0 and applications > 0:
            return ((interviews + offers) / applications)
        else:
            return 0

    @staticmethod
    def calculate_conversion_score(applications, interviews, offers):
        if interviews + offers > 0 and applications > 0:
            return ((interviews + (offers * 2)) / applications)
        else:
            return 0
