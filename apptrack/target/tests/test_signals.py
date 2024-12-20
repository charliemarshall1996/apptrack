"""Tests for target signals.

This module contains tests for the target signals.
test_create_target_on_profile_creation tests that a target is created when a profile is
created.
"""

import pytest

from target.models import Target


@pytest.mark.django_db
def test_create_target_on_profile_creation(profile_factory):
    profile = profile_factory()
    profile.save()

    assert Target.objects.filter(profile=profile).exists()
