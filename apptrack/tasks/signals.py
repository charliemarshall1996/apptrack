
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from targets.models import Target
from .models import TargetTask


@receiver(post_save, sender=Target)
def create_target_task_on_reset(sender, instance, created, **kwargs):
    task_name = f"Target for {timezone.now().date()}"
    if not created:  # Only check on update, not creation
        # Fetch the old value of `last_reset`
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.last_reset != instance.last_reset:
            # Create a new TargetTask if `last_reset` changed
            TargetTask.objects.create(target=instance, name=task_name)
    else:
        TargetTask.objects.create(
            target=instance, name=task_name)
