
from django.utils import timezone
import pytest

from accounts.models import CustomUser, Profile, Streak


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
def test_target():
    pass


@pytest.mark.django_db
def test_target_met():
    pass


@pytest.mark.django_db
def test_target_not_met():
    pass


@pytest.mark.django_db
def test_target_reset_no_target():
    pass


@pytest.mark.django_db
def test_target_reset_same_day():
    pass


@pytest.mark.django_db
def test_target_reset_new_day_met():
    pass


@pytest.mark.django_db
def test_target_reset_new_day_not_met():
    pass


@pytest.mark.django_db
def test_target_increment():
    pass


@pytest.mark.django_db
def test_target_decrement():
    pass


@pytest.mark.django_db
def test_target_changed():
    pass
