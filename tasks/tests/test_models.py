"""Tests for tasks models."""

import pytest

from tasks.models import Task


@pytest.mark.django_db
def test_task(profile_factory):
    """Test task model."""
    # Initialise data
    name = "Test Task"
    priority = 1
    is_completed = False
    profile = profile_factory()
    profile.save()

    # Create a task
    task = Task(
        profile=profile, name=name, priority=priority, is_completed=is_completed
    )
    task.save()

    assert task.priority == priority
    assert task.is_completed == is_completed
    assert task.name == name
    assert task.profile == profile
