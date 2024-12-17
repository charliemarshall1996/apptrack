
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import post_save
from django.dispatch import receiver
from target.models import target_reset, Target

from .models import TargetTask


@receiver(target_reset)
def create_target_task_on_reset(sender, instance, **kwargs):
    task_name = "Daily Applications Target"
    profile = instance.profile

    task, created = TargetTask.objects.get_or_create(
        profile=profile, target=instance)

    task.is_completed = False
    task.name = task_name

    task.save()


@receiver(post_save, sender=Target)
def check_target_task(sender, instance, **kwargs):

    try:
        task, _ = TargetTask.objects.get_or_create(
            target=instance, profile=instance.profile)
    except MultipleObjectsReturned:
        # If multiple objects exist, retain the first and delete the rest
        tasks = TargetTask.objects.filter(
            target=instance, profile=instance.profile)
        # Get the first task
        task = tasks.first()
        # Delete the other tasks
        tasks.exclude(id=task.id).delete()

    print("task: ", task)
    print("target: ", instance)
    task.save()
