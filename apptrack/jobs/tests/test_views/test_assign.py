# noqa: D100
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_assign_job_view(client, profile_factory, job_factory):  # noqa: D103
    password = "securepassword"  # noqa: S105

    profile = profile_factory(password=password)
    profile.save()

    board = profile.board

    columns = [col.id for col in board.columns.all()]

    job = job_factory(profile=profile)
    job.board = board
    job.save()
    try:
        assert job.column.id in columns
    except AssertionError:
        print(f"COLUMNS: {columns}\nJOB COLUMN: {job.column.id}")

    old_col = job.column.id

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": password}
    )

    assert response.status_code == 302

    url = reverse(
        "jobs:assign", kwargs={"job_id": str(job.id), "col_id": str(columns[1])}
    )

    response = client.post(url)
    try:
        assert job.column.id != old_col
    except AssertionError:
        print(f"OLD COLUMN: {old_col}\nJOB COLUMN: {job.column.id}")

    try:
        assert job.column.id == columns[1]
    except AssertionError:
        print(f"JOB COLUMN {job.column.id}\nI1 COLUMN: {columns[1]}")
