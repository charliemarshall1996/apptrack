"""Tests for target models."""

import datetime
from unittest.mock import Mock, patch

from django.utils import timezone
import pytest

from target.models import Target, Streak


@pytest.mark.django_db
def test_streak():  # noqa: D103
    streak = Streak()
    streak.save()
    assert streak.current_streak_start.date() == timezone.now().date()
    assert streak.current_streak == 0
    assert streak.longest_streak == 0
    assert not streak.longest_streak_start
    assert not streak.longest_streak_end


@pytest.mark.django_db
def test_streak_increment():  # noqa: D103
    """Test the Streak model increment method increments the current_streak by 1."""
    streak = Streak()
    streak.save()

    streak.increment()
    assert streak.current_streak == 1


@pytest.mark.django_db
def test_streak_reset_new_longest():
    """Streak model reset method with new longest streak."""
    streak = Streak()
    streak.save()
    streak.increment()
    streak.reset()

    assert streak.current_streak == 0
    assert streak.longest_streak_start.date() == timezone.now().date()
    assert streak.longest_streak_end.date() == timezone.now().date()
    assert streak.longest_streak == 1
    assert streak.current_streak_start.date() == timezone.now().date()


@pytest.mark.django_db
def test_streak_reset_not_new_longest():
    """Streak model reset method with no new longest streak."""
    streak = Streak(longest_streak=2)
    streak.save()
    streak.increment()
    streak.reset()

    assert streak.current_streak == 0
    assert streak.longest_streak == 2
    assert streak.current_streak_start.date() == timezone.now().date()


# TODO: Need to change this to manually create a target
@pytest.mark.django_db
def test_target(profile_factory):  # noqa: D103
    profile = profile_factory()
    profile.save()

    assert Target.objects.filter(profile=profile).exists()

    target = Target.objects.get(profile=profile)
    assert target.profile == profile
    assert target.amount == 5
    assert target.current == 0
    assert target.streak
    assert target.total_targets_met == 0
    assert target.last_reset.date() == timezone.now().date()


@pytest.mark.django_db
def test_target_met(profile_factory):
    """Target model met property where current >= amount.

    Ensures that if current >= amount, the target is True.
    """
    profile = profile_factory()
    profile.save()

    # Assert a target has been created
    assert Target.objects.filter(profile=profile).exists()

    target = Target.objects.get(profile=profile)

    # Target resets current if
    # amount is changed
    target.amount = 1
    target.save()
    target.current = 1
    target.save()

    # Assert the target is met
    assert target.met


@pytest.mark.django_db
def test_target_not_met(profile_factory):
    """Target model met property where current < amount.

    Ensures that if current < amount, the target is False.
    """
    profile = profile_factory()
    profile.save()

    # Assert a target has been created
    assert Target.objects.filter(profile=profile).exists()

    target = Target.objects.get(profile=profile)

    # Target resets current if
    # amount is changed
    target.amount = 1
    target.save()

    # Assert the target is met
    assert not target.met


@pytest.mark.django_db
def test_target_reset_does_not_call_save(profile_factory):
    """Target model reset method called where from_save is False.

    Ensures that the target.save() method is not called if from_save=False.
    """
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.current = 1
    target.save()
    mock_save = Mock()

    with patch("target.models.Target.save", mock_save):
        target.last_reset = timezone.now() - datetime.timedelta(days=1)
        target.reset(from_save=True)
    mock_save.assert_not_called()


@pytest.mark.django_db
def test_target_reset_does_call_save(profile_factory):
    """Target model reset called where from_save is True.

    Ensures that if the reset method is called with from_save=True,
    the target.save() method is called.
    """
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.current = 1
    target.save()

    mock_save = Mock()
    with patch("target.models.Target.save", mock_save):
        target.last_reset = timezone.now() - datetime.timedelta(days=1)
        target.reset(from_save=False)
    mock_save.assert_called()


@pytest.mark.django_db
def test_target_reset_target_amount_zero(profile_factory):
    """Target model reset method with no target total_targets_met.

    Ensures that if the reset method is called on a target with amount 0,
    total_targets_met does not increment.
    """
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.reset()

    assert target.total_targets_met == 0


@pytest.mark.django_db
def test_target_reset_same_day(profile_factory):
    """Target model reset method called with same day as last_reset.

    Ensures that if the reset method is called on the same day as the last
    reset, the total_targets_met does not increment.
    """
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.reset()
    assert target.total_targets_met == 0


@pytest.mark.django_db
def test_target_reset_new_day_met(profile_factory):
    """Target model reset method with new day and met.

    Ensures that if the reset method is called on a new day and the target
    is met, the total_targets_met and streak.current_streak do increment.
    """
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.last_reset = timezone.now() - datetime.timedelta(days=1)
    target.current = 1
    target.save()

    target.reset()
    assert target.total_targets_met == 1
    assert target.streak.current_streak == 1


@pytest.mark.django_db
def test_target_reset_new_day_not_met(profile_factory):
    """Test the Target model reset method with new day and not met.

    Ensures that if the reset method is called on a new day and the target
    is not met, the total_targets_met and streak.current_streak do not
    increment.
    """
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.last_reset = timezone.now() - datetime.timedelta(days=1)
    target.save()

    target.reset()
    assert target.total_targets_met == 0
    assert target.streak.current_streak == 0


@pytest.mark.django_db
def test_target_increment(profile_factory):
    """Test the Target model increment method.

    Ensures that when the increment method is called,
    the current value is incremented.
    """
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()

    # When increment is called
    # current will be incremented
    target.increment()
    assert target.current == 1


@pytest.mark.django_db
def test_target_decrement(profile_factory):
    """Test the Target model decrement method.

    Ensures that when the decrement method is called,
    the current value is decremented.
    """
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.current = 1
    target.save()

    # When decrement is called
    # current will be decremented
    target.decrement()
    assert target.current == 0
