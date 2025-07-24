import pytest
from interviews.forms import AddInterviewForm
from interviews.models import Interview


@pytest.mark.django_db
def test_add_interview_form(interview_data_factory):
    # initialise data
    data = interview_data_factory()
    data["job"].save()
    data.pop("profile")

    form = AddInterviewForm(data=data)

    try:
        interview = form.save()
        assert isinstance(interview, Interview)
    except (AssertionError, ValueError):
        print(form.errors)
        raise AssertionError
