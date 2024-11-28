
import pytest
from jobs.models import Board


@pytest.mark.django_db
def test_board_created_on_user_creation(custom_user_factory):
    user = custom_user_factory()
    user.save()

    board = Board.objects.get(user=user)
    assert board
    assert board.name == "My Job Board"
