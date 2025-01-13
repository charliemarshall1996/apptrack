# noqa: D100
import logging

import pytest

from jobs.models import (
    Job,
    Column,
    Interview,
    Reminder,
    JobFunction,
    LocationPolicy,
    PayRate,
    WorkContract,
)
from core.choices import StatusChoices
from tasks.models import InterviewTask

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_board(profile_factory):
    profile = profile_factory()
    profile.save()
    board = profile.board
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
        ("Open", 1),
        ("Applied", 2),
        ("Shortlisted", 3),
        ("Interview", 4),
        ("Offer", 5),
        ("Rejected", 6),
        ("Closed", 7),
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
def test_job(profile_factory, column_factory, job_data_factory):
    data = job_data_factory()
    profile = profile_factory()
    profile.save()
    board = profile.board
    column = column_factory(board=board)
    job = Job(profile=profile, column=column, board=board, **data)

    assert job.description == data["description"]
    assert job.company == data["company"]
    assert job.source == data["source"]
    assert job.city == data["city"]
    assert job.job_title == data["job_title"]
    assert job.min_pay == data["min_pay"]
    assert job.max_pay == data["max_pay"]
    assert job.note == data["note"]
    assert job.url == data["url"]
    assert job.status == data["status"]

    assert job.column.name == column.name
    assert job.column.position == column.position
    assert job.column.board.name == board.name


@pytest.mark.django_db
def test_job_updated(profile_factory, column_factory, job_data_factory):
    profile = profile_factory()
    profile.save()
    board = profile.board
    column = column_factory(board=board)
    job = Job(profile=profile, column=column,
              board=board, **job_data_factory())

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
def test_job_status_no_column(profile_factory, job_data_factory):
    profile = profile_factory()
    profile.save()
    board = profile.board
    job = Job(profile=profile, board=board, **job_data_factory())
    job.save()

    assert job.column
    assert StatusChoices.get_status_name(job.status) == job.column.name
    assert StatusChoices.get_status_column_position(
        job.status) == job.column.position


@pytest.mark.django_db
def test_job_status_applied(profile_factory, job_data_factory):
    applied_statuses = StatusChoices.get_applied_statuses()
    data = job_data_factory()
    for status in applied_statuses:
        data["status"] = StatusChoices.OPEN[0]
        logger.info("status: %s", status)
        logger.info("jobs_data: %s", data)
        profile = profile_factory()
        profile.save()
        board = profile.board
        job = Job(profile=profile, board=board, **data)
        job.save()

        assert not job.applied
        job.status = status
        logger.info("job.status: %s", job.status)
        job.save()
        assert job.status == status
        assert job.applied


@pytest.mark.django_db
def test_interview(interview_data_factory):
    data = interview_data_factory()
    job = data["job"]
    profile = job.profile

    interview = Interview(**data)

    assert interview.job == job
    assert interview.profile == profile
    assert interview.round == data["round"]
    assert interview.start_date == data["start_date"]
    assert interview.end_date == data["end_date"]
    assert interview.post_code == data["post_code"]
    assert interview.building == data["building"]
    assert interview.street == data["street"]
    assert interview.city == data["city"]
    assert interview.region == data["region"]
    assert interview.notes == data["notes"]
    assert str(interview) == f"Interview for {job.job_title} at {job.company}"


@pytest.mark.django_db
def test_interview_creates_default_tasks(interview_factory):
    interview = interview_factory()
    interview.job.save()
    interview.profile.user.save()
    interview.profile.save()
    interview.save()

    assert interview

    default_tasks = [
        "Prepare for interview",
        "Review job description",
        "Research the company",
        "Prepare questions for the interviewer",
        "Dress appropriately",
        "Plan your route to the interview",
    ]

    for task in default_tasks:
        assert InterviewTask.objects.filter(
            interview=interview, name=task).exists()


@pytest.mark.django_db
def test_interview_task(interview_task_data_factory):
    data = interview_task_data_factory()
    interview = data["interview"]

    task = InterviewTask(**data)

    assert task.interview == interview
    assert task.name == data["name"]
    assert task.is_completed == data["is_completed"]


@pytest.mark.django_db
def test_reminder(reminder_data_factory):
    data = reminder_data_factory()
    reminder = Reminder.objects.create(**data)
    assert reminder.offset == data["offset"]
    assert reminder.unit == data["unit"]
    assert reminder.profile == data["profile"]
    assert not reminder.emailed
    assert not reminder.read


@pytest.mark.django_db
def test_job_function():
    code = "TE"
    name = "TEST"

    job_function = JobFunction(code=code, name=name)
    job_function.save()

    assert job_function.code == code
    assert job_function.name == name
    assert str(job_function) == name


@pytest.mark.django_db
def test_location_policy():
    code = "TE"
    name = "TEST"

    location_policy = LocationPolicy(code=code, name=name)
    location_policy.save()

    assert location_policy.code == code
    assert location_policy.name == name


@pytest.mark.django_db
def test_pay_rate():
    code = "TE"
    name = "TEST"

    pay_rate = PayRate(code=code, name=name)
    pay_rate.save()

    assert pay_rate.code == code
    assert pay_rate.name == name


@pytest.mark.django_db
def test_work_contract():
    code = "TE"
    name = "TEST"

    work_contract = WorkContract(code=code, name=name)
    work_contract.save()

    assert work_contract.code == code
    assert work_contract.name == name
