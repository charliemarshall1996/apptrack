
import logging

import pytest

from jobs.models import Job, Column, Board
from jobs.choices import StatusChoices

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_board(custom_user_factory):
    user = custom_user_factory()
    board = user.board
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
def test_job(custom_user_factory, column_factory, jobs_data):
    user = custom_user_factory()
    board = user.board
    column = column_factory(board=board)
    job = Job(user=user, column=column, board=board, **jobs_data)

    assert job.description == jobs_data["description"]
    assert job.company == jobs_data["company"]
    assert job.source == jobs_data["source"]
    assert job.city == jobs_data["city"]
    assert job.job_title == jobs_data["job_title"]
    assert job.min_pay == jobs_data["min_pay"]
    assert job.max_pay == jobs_data["max_pay"]
    assert job.note == jobs_data["note"]
    assert job.url == jobs_data["url"]
    assert job.status == jobs_data["status"]

    assert job.column.name == column.name
    assert job.column.position == column.position
    assert job.column.board.name == board.name


@pytest.mark.django_db
def test_job_updated(custom_user_factory, column_factory, jobs_data):
    user = custom_user_factory()
    board = user.board
    column = column_factory(board=board)
    job = Job(user=user, column=column, board=board, **jobs_data)

    job.save()

    original_updated = job.updated
    statuses = [
        StatusChoices.APPLIED,
        StatusChoices.SHORTLISTED,
        StatusChoices.INTERVIEW,
        StatusChoices.OFFER,
        StatusChoices.REJECTED,
        StatusChoices.CLOSED,
    ]
    i = 0
    for status in statuses:
        logger.info("status: %s", status)
        job.status = status[0]
        job.save()
        if i > 0:
            assert original_updated
            assert job.updated > original_updated
        else:
            assert job.updated
        original_updated = job.updated
        i += 1


@pytest.mark.django_db
def test_job_status_no_column(custom_user_factory, jobs_data):
    user = custom_user_factory()
    board = user.board
    job = Job(user=user, board=board, **jobs_data)
    job.save()

    assert job.column
    assert StatusChoices.get_status_name(job.status) == job.column.name
    assert StatusChoices.get_status_column_position(
        job.status) == job.column.position


@pytest.mark.django_db
def test_job_status_applied(custom_user_factory, jobs_data):
    applied_statuses = StatusChoices.get_applied_statuses()

    for status in applied_statuses:
        jobs_data["status"] = StatusChoices.OPEN[0]
        logger.info("status: %s", status)
        logger.info("jobs_data: %s", jobs_data)
        user = custom_user_factory()
        board = user.board
        job = Job(user=user, board=board, **jobs_data)
        job.save()

        assert not job.applied
        job.status = status
        logger.info("job.status: %s", job.status)
        job.save()
        assert job.status == status
        assert job.applied
