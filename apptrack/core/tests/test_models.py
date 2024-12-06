
import pytest

from core.models import Task, Alert


@pytest.mark.django_db
def test_task_model():
    task = Task.objects.create(name="Test Task")
    assert str(task) == "Test Task"
    assert task.is_completed is False
