
from django.dispatch import receiver
from django.utils import timezone
from targets.models import target_reset

from .models import TargetTask, Task


@receiver(target_reset)
def create_target_task_on_reset(sender, instance, **kwargs):
    task_name = f"Target for {timezone.now().date()}"
    user = instance.profile.user
    task = TargetTask(target=instance, name=task_name, user=user)
    task.save()
