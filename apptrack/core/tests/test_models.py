
import pytest

from core.models import Task, Reminder


@pytest.mark.django_db
def test_task_model(task_data_factory):
    data = task_data_factory()
    task = Task.objects.create(**data)
    assert str(task) == data['name']
    assert task.is_completed is False


@pytest.mark.django_db
def test_alert_model(reminder_data_factory):
    data = reminder_data_factory()
    reminder = Reminder.objects.create(**data)
    assert reminder.offset == data["offset"]
    assert reminder.unit == data["unit"]
    assert reminder.user == data["user"]
    assert not reminder.emailed
    assert not reminder.read
