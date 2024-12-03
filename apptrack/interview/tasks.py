# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Interview

from webpush import send_user_notification


@shared_task
def send_push_notification(user_id, payload):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(id=user_id)

    try:
        send_user_notification(user=user, payload=payload, ttl=1000)
        return f"Notification sent to user {user.email}"
    except Exception as e:
        # Handle errors gracefully
        return f"An error occurred: {str(e)}"


@shared_task
def check_upcoming_interviews():
    now = timezone.now()
    upcoming_interviews = Interview.objects.filter(start_time__gt=now)

    for i in upcoming_interviews:
        user = i.user
        start_time = i.start_time
        for alert in i.alerts:
            if not alert.read or alert.persistent:
                unit = alert.alert_before_unit
                alert_time = (
                    start_time - timedelta(days=alert.alert_before) if unit == "d" else
                    start_time - timedelta(hours=alert.alert_before) if unit == "h" else
                    start_time - timedelta(minutes=alert.alert_before)
                )

                if alert_time <= now and alert.alert_via_push:
                    payload = {
                        "head": "Interview Reminder",
                        "body": f"{alert.message}",
                        "icon": "/static/images/notification-icon.png",
                        "url": "/interviews/"  # URL to redirect on notification click
                    }
                    send_push_notification.delay(user.id, payload)

                if alert.alert_via_email and not alert.emailed:
                    subject = "AppTrack Interview Reminder"
                    message = f"{alert.message}"
                    html_message = f"<p>{alert.message}</p>"
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                              [user.email], html_message=html_message)
