from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Boards

User = get_user_model()


@receiver(post_save, sender=User)
def create_board_for_new_user(sender, instance, created, **kwargs):
    if created:
        # Create a default board for the new user
        Boards.objects.create(
            user=instance, name=f"My Job Board")
