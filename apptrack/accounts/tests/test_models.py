
import datetime
from unittest.mock import Mock, patch

from django.utils import timezone
import pytest

from accounts.models import CustomUser, Profile, Streak, Target


@pytest.mark.django_db
def test_custom_user(custom_user_data_factory):
    data = custom_user_data_factory()
    model = CustomUser(**data)
    assert model.email == data['email']
    assert model.email_verified == data['email_verified']
    assert model.last_verification_email_sent == data[
        'last_verification_email_sent']
    assert model.first_name == data['first_name']
    assert model.last_name == data['last_name']
    assert model.is_active == data['is_active']
    assert model.is_staff == data['is_staff']
    assert model.date_joined == data['date_joined']
    assert str(model) == data["email"]


@pytest.mark.django_db
def test_profile(custom_user_factory, profile_data_factory):
    user = custom_user_factory()
    data = profile_data_factory(user)
    model = Profile(**data)
    assert model.user == data['user']
    assert model.email_comms_opt_in == data['email_comms_opt_in']
    assert model.birth_date == data['birth_date']
    assert str(model) == user.email


@pytest.mark.django_db
def test_streak():
    streak = Streak()
    streak.save()
    assert streak.current_streak_start.date() == timezone.now().date()
    assert streak.current_streak == 0
    assert streak.longest_streak == 0
    assert not streak.longest_streak_start
    assert not streak.longest_streak_end


@pytest.mark.django_db
def test_streak_increment():
    streak = Streak()
    streak.save()

    assert streak.current_streak_start.date() == timezone.now().date()
    assert streak.current_streak == 0
    assert streak.longest_streak == 0
    assert not streak.longest_streak_start
    assert not streak.longest_streak_end

    streak.increment()
    assert streak.current_streak == 1


@pytest.mark.django_db
def test_streak_reset_new_longest():
    streak = Streak()
    streak.save()

    assert streak.current_streak_start.date() == timezone.now().date()
    assert streak.current_streak == 0
    assert streak.longest_streak == 0
    assert not streak.longest_streak_start
    assert not streak.longest_streak_end

    streak.increment()
    assert streak.current_streak == 1

    streak.reset()
    assert streak.current_streak == 0
    assert streak.longest_streak_start.date() == timezone.now().date()
    assert streak.longest_streak_end.date() == timezone.now().date()
    assert streak.longest_streak == 1
    assert streak.current_streak_start.date() == timezone.now().date()


@pytest.mark.django_db
def test_streak_reset_not_new_longest():
    streak = Streak(longest_streak=2)
    streak.save()

    assert streak.current_streak_start.date() == timezone.now().date()
    assert streak.current_streak == 0
    assert streak.longest_streak == 2
    assert not streak.longest_streak_start
    assert not streak.longest_streak_end

    streak.increment()
    assert streak.current_streak == 1

    streak.reset()
    assert streak.current_streak == 0
    assert streak.longest_streak == 2
    assert streak.current_streak_start.date() == timezone.now().date()


@pytest.mark.django_db
def test_target(profile_factory):
    profile = profile_factory()
    profile.save()

    # Assert a target has been created
    assert Target.objects.filter(profile=profile).exists()

    target = Target.objects.get(profile=profile)
    assert target.profile == profile
    assert target.amount == 0
    assert target.current == 0
    assert target.streak
    assert target.total_targets_met == 0
    assert target.last_reset.date() == timezone.now().date()


@pytest.mark.django_db
def test_target_met(profile_factory):
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
    assert target.profile == profile
    assert target.amount == 1
    assert target.current == 1
    assert target.streak
    assert target.total_targets_met == 0
    assert target.last_reset.date() == timezone.now().date()

    # Assert the target is met
    assert target.met


@pytest.mark.django_db
def test_target_not_met(profile_factory):
    profile = profile_factory()
    profile.save()

    # Assert a target has been created
    assert Target.objects.filter(profile=profile).exists()

    target = Target.objects.get(profile=profile)

    # Target resets current if
    # amount is changed
    target.amount = 1
    target.save()
    assert target.profile == profile
    assert target.amount == 1
    assert target.current == 0
    assert target.streak
    assert target.total_targets_met == 0
    assert target.last_reset.date() == timezone.now().date()

    # Assert the target is met
    assert not target.met


@pytest.mark.django_db
def test_target_reset_does_not_call_save(profile_factory):
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.current = 1
    target.save()
    mock_save = Mock()

    with patch('accounts.models.Target.save', mock_save):
        target.last_reset = timezone.now() - datetime.timedelta(days=1)
        target.reset(from_save=True)
    mock_save.assert_not_called()


@pytest.mark.django_db
def test_target_reset_does_call_save(profile_factory):
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.current = 1
    target.save()

    mock_save = Mock()
    with patch('accounts.models.Target.save', mock_save):
        target.last_reset = timezone.now() - datetime.timedelta(days=1)
        target.reset(from_save=False)
    mock_save.assert_called()


@pytest.mark.django_db
def test_target_reset_no_target(profile_factory):
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)

    # If no target,
    # total_targets_met
    # won't increment

    target.reset()
    assert target.total_targets_met == 0


@pytest.mark.django_db
def test_target_reset_same_day(profile_factory):
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()

    # If same day,
    # total_targets_met
    # won't increment

    target.reset()
    assert target.total_targets_met == 0


@pytest.mark.django_db
def test_target_reset_new_day_met(profile_factory):
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.last_reset = timezone.now() - datetime.timedelta(days=1)
    target.current = 1
    target.save()

    # If new day,
    # and met,
    # total_targets_met
    # and streak.current_streak
    # will increment

    target.reset()
    assert target.total_targets_met == 1
    assert target.streak.current_streak == 1


@pytest.mark.django_db
def test_target_reset_new_day_not_met(profile_factory):
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.last_reset = timezone.now() - datetime.timedelta(days=1)
    target.save()

    # If new day,
    # and not met,
    # total_targets_met
    # and streak.current_streak
    # will not increment

    target.reset()
    assert target.total_targets_met == 0
    assert target.streak.current_streak == 0


@pytest.mark.django_db
def test_target_increment(profile_factory):
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


@pytest.mark.django_db
def test_target_changed(profile_factory):
    profile = profile_factory()
    profile.save()

    target = Target.objects.get(profile=profile)
    target.amount = 1
    target.save()
    target.current = 1
    target.save()

    target.amount = 2
    target.save()

    # When amount is changed
    # current will be reset
    assert target.current == 0
