
from django.dispatch import receiver
from targets.models import target_reset

from .models import TargetTask


@receiver(target_reset)
def create_target_task_on_reset(sender, instance, **kwargs):
    task_name = f"Daily Applications Target"
    user = instance.profile.user

    task, created = TargetTask.objects.get_or_create(
        user=user, target=instance)

    task.is_completed = False
    task.name = task_name

    task.save()
