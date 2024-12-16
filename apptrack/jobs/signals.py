
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from accounts.models import target_reset, Profile, Target

from .apps import JobsConfig
from .choices import JobFunctionChoices
from .models import Board, Column, TargetTask, JobFunction


@receiver(target_reset)
def create_target_task_on_reset(sender, instance, **kwargs):
    task_name = "Daily Applications Target"
    profile = instance.profile

    task, created = TargetTask.objects.get_or_create(
        profile=profile, target=instance)

    task.is_completed = False
    task.name = task_name

    task.save()


@receiver(post_save, sender=Profile)
def create_board(sender, instance, created, **kwargs):
    if created:
        board = Board.objects.create(profile=instance, name='My Job Board')
        board.save()


@ receiver(post_save, sender=Board)
def create_columns(sender, instance, created, **kwargs):

    default_columns = [
        ('Open', 1),
        ('Applied', 2),
        ('Shortlisted', 3),
        ('Interview', 4),
        ('Offer', 5),
        ('Rejected', 6),
        ('Closed', 7),
    ]

    if created and not instance.columns.exists():
        for name, position in default_columns:
            column = Column.objects.create(
                board=instance, name=name, position=position)
            column.save()


@receiver(post_migrate, sender=JobsConfig)
def post_migration(sender, instance, *args, **kwargs):
    for code, name in JobFunctionChoices.choices():
        JobFunction.objects.get_or_create(code=code, name=name)


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
