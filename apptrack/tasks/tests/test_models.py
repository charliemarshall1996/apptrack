"""Tests for tasks models."""

import pytest

from tasks.models import Task, TargetTask


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


@pytest.mark.django_db
def test_target_task(profile_factory):
    """Test target task model."""
    # Initialise data
    name = "Test Task"
    priority = 1
    is_completed = False
    profile = profile_factory()
    profile.save()
    amount = 1
    target = profile.target
    target.amount = amount
    target.current = 0
    target.save()

    # Create a task
    task = TargetTask(
        profile=profile,
        target=target,
        name=name,
        priority=priority,
        is_completed=is_completed,
    )
    task.save()

    assert task.priority == priority
    assert not task.is_completed
    assert task.name == name
    assert task.target == target
    assert task.current_val == 0
    assert task.target_val == amount
    assert task.type == "target"


@pytest.mark.django_db
def test_target_task_save_met(profile_factory):
    """Test target task model.

    Test that is_completed is set to True when current_val == target_val
    """
    # Initialise data
    name = "Test Task"
    priority = 1
    is_completed = False
    profile = profile_factory()
    profile.save()
    amount = 1
    target = profile.target
    target.current = 0
    target.amount = amount
    target.save()

    # Create a task
    task = TargetTask(
        profile=profile,
        target=target,
        name=name,
        priority=priority,
        is_completed=is_completed,
    )
    task.save()

    target.increment()

    task.save()

    assert task.current_val == 1
    assert task.is_completed
