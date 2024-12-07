
import pytest

from interview.models import Interview


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
    assert interview.town == data["town"]
    assert interview.region == data["region"]
    assert interview.country == data["country"]
    assert interview.notes == data["notes"]
    assert str(interview) == f"Interview for {job.job_title} at {job.company}"
