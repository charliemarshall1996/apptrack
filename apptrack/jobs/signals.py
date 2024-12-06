
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Board, Column

User = get_user_model()


@receiver(post_save, sender=User)
def create_board(sender, instance, created, **kwargs):
    if created:
        print(f"Signal triggered for user: {instance.email}")
        board = Board.objects.create(user=instance, name='My Job Board')
        board.save()
        print(f"BOARD NAME: {board.name}")
        print(f"BOARD USER EMAIL: {board.user.email}")


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
