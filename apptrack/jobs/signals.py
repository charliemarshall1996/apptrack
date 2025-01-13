"""This module contains the signals for the jobs app.

The create_board_on_profile_creation function is called when a new profile is created,
creating a corresponding board for the profile instance. The 
create_columns_on_board_creation function is called when a new board is created,
creating default columns for the board.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile

from .models import Board, Column


@receiver(post_save, sender=Profile)
def create_board_on_profile_creation(sender, instance, created, **kwargs):  # noqa: D103
    if created:
        board = Board.objects.create(profile=instance, name="My Job Board")
        board.save()


@receiver(post_save, sender=Board)
def create_columns_on_board_creation(sender, instance, created, **kwargs):  # noqa: D103
    default_columns = [
        ("Open", 1),
        ("Applied", 2),
        ("Shortlisted", 3),
        ("Interview", 4),
        ("Offer", 5),
        ("Rejected", 6),
        ("Closed", 7),
    ]

    if created and not instance.columns.exists():
        for name, position in default_columns:
            column = Column.objects.create(
                board=instance, name=name, position=position)
            column.save()
