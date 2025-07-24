
import pytest
from interviews.models import Interview
from tasks.models import InterviewTask


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
