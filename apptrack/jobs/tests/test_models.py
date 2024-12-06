
import pytest

from jobs.models import Job, Column, Board


@pytest.mark.django_db
def test_board(board_factory):
    board = board_factory(no_name=True)
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
    expected_columns = [
        ('Open', 1),
        ('Applied', 2),
        ('Shortlisted', 3),
        ('Interview', 4),
        ('Offer', 5),
        ('Rejected', 6),
        ('Closed', 7),
    ]

    for name, position in expected_columns:
        assert Column.objects.filter(
            name=name, position=position, board=board).exists()


@pytest.mark.django_db
def test_column(board_factory, column_data_factory):
    board = board_factory()
    data = column_data_factory(board=board)
    column = Column(**data)
    assert column.name == data["name"]
    assert column.position == data["position"]
    assert column.board.name == board.name
    assert column.board.id == board.id


@pytest.mark.django_db
def test_job(custom_user_factory, board_factory, column_factory, jobs_data):
    user = custom_user_factory()
    board = board_factory(user=user)
    column = column_factory(board=board)
    job = Job(user=user, column=column, board=board, **jobs_data)

    assert job.description == jobs_data["description"]
    assert job.company == jobs_data["company"]
    assert job.source == jobs_data["source"]
    assert job.town == jobs_data["town"]
    assert job.country == jobs_data["country"]
    assert job.job_title == jobs_data["job_title"]
    assert job.min_pay == jobs_data["min_pay"]
    assert job.max_pay == jobs_data["max_pay"]
    assert job.work_contract == jobs_data["work_contract"]
    assert job.location_policy == jobs_data["location_policy"]
    assert job.note == jobs_data["note"]
    assert job.url == jobs_data["url"]
    assert job.job_function == jobs_data["job_function"]
    assert job.status == jobs_data["status"]

    assert job.column.name == column.name
    assert job.column.position == column.position
    assert job.column.board.name == board.name
