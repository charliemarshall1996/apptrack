"""Tasks signals."""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from interviews.models import Interview
from .models import InterviewTask

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Interview)
def create_tasks_on_interview_creation(sender, instance, created, **kwargs):
    """Create tasks when an interview is created."""
    logger.debug("Interview saved: %s", instance)
    if created:
        logger.debug("Interview is new. Creating tasks...")
        default_tasks = [
            "Prepare for interview",
            "Review job description",
            "Research the company",
            "Prepare questions for the interviewer",
            "Dress appropriately",
            "Plan your route to the interview",
        ]
        for task in default_tasks:
            logger.debug("Creating task: %s", task)

            try:
                InterviewTask.objects.create(
                    interview=instance, profile=instance.profile, name=task
                )
            except Exception as e:
                logger.error("Error creating task: %s", e)
                raise e
