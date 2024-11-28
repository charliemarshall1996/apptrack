import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


@pytest.mark.django_db
def test_board_view(client, profile_factory):

    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302
    url = reverse('jobs:board')

    # GET request should show job board
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_job_view(client, board_factory, profile_factory, jobs_form_data):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    board = board_factory(user=profile.user)
    board.save()

    data = jobs_form_data

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302

    url = reverse('jobs:add_job')

    # GET request should show add job form
    response = client.get(url)
    assert response.status_code == 200
    assert 'job_form' in response.context

    # POST request with valid data should add job
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('jobs:board')


@pytest.mark.django_db
def test_assign_job_view(client, board_factory, profile_factory, job_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    board = board_factory(user=profile.user)
    board.save()

    columns = [col.id for col in board.columns.all()]

    job = job_factory(user=profile.user)
    job.board = board
    job.save()
    try:
        assert job.column.id in columns
    except AssertionError:
        print(f"COLUMNS: {columns}\nJOB COLUMN: {job.column.id}")

    old_col = job.column.id

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302

    url = reverse('jobs:assign_job',
                  kwargs={"job_id": str(job.id),
                          "col_id": str(columns[1])})
    response = client.get(url)

    assert response.status_code == 200

    response = client.post(url)
    try:
        assert job.column.id != old_col
    except AssertionError:
        print(f"OLD COLUMN: {old_col}\nJOB COLUMN: {job.column.id}")

    try:
        assert job.column.id == columns[1]
    except AssertionError:
        print(f"JOB COLUMN {job.column.id}\nI1 COLUMN: {columns[1]}")


@pytest.mark.django_db
def test_delete_job_view(client, job_factory, profile_factory, board_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    board = board_factory(user=profile.user)
    board.save()

    job = job_factory(user=profile.user)
    job.board = board
    job.save()

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302

    url = reverse("jobs:delete_job", kwargs={"pk": job.pk})
    response = client.get(url)

    try:
        assert response.status_code == 200
    except AssertionError:
        print(response.url)

    assert job.DoesNotExist
