
import pytest

from jobs.models import Jobs, Boards, Columns


@pytest.mark.django_db
def test_board(board_factory):
    board = board_factory()
    board.save()
    board_columns = [column.name for column in board.columns.all()]
    assert board.name == "My Job Board"
    assert "Open" in board_columns
    assert "Applied" in board_columns
    assert "Shortlisted" in board_columns
    assert "Interview" in board_columns
    assert "Offer" in board_columns
    assert "Rejected" in board_columns
    assert "Closed" in board_columns


@pytest.mark.django_db
def test_column(board_factory, column_data_factory):
    board = board_factory()
    data = column_data_factory(board=board)
    column = Columns(board=board, **data)
    assert column.name == data["name"]
    assert column.position == data["position"]
    assert column.board.name == board.name
    assert column.board.id == board.id


@pytest.mark.django_db
def test_job(custom_user_factory, board_factory, column_data_factory, jobs_form_data):
    user = custom_user_factory()
    board = board_factory(user=user)
    job = Jobs(user=user, **jobs_form_data)
