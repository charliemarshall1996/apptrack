
import pytest

from interview.models import (Interview,
                              InterviewTask)


@pytest.mark.django_db
def test_interview(interview_data_factory):
    data = interview_data_factory()
    job = data['job']
    user = data['user']

    interview = Interview(**data)

    assert interview.job == job
    assert interview.user == user
    assert interview.interview_round == data['interview_round']
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
    interview.user.save()
    interview.save()

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
    interview = data['interview']

    task = InterviewTask(**data)

    assert task.interview == interview
    assert task.name == data['name']
    assert task.is_completed == data['is_completed']
