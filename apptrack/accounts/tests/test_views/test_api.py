import pytest

from accounts.views import ProfileAPI


@pytest.mark.django_db
def test_api_view(client, profile_factory):
    profile = profile_factory()
    profile.save()

    api = ProfileAPI()

    response = api.get(request=None, id=profile.id)

    print(response)
    assert response.status_code == 200

    data = response.data
    assert data["basic_stats"] == api._get_basic_stats(profile)


@pytest.mark.django_db
def test_api_view_total_applications(client, profile_factory):
    pass
