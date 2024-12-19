import pytest

from target.models import Target


@pytest.mark.django_db
def test_create_target_on_profile_creation(profile_factory):
    profile = profile_factory()
    profile.save()

    assert Target.objects.filter(profile=profile).exists()
