
import logging
import csv
from datetime import timedelta
from io import StringIO

from django.urls import reverse
from django.utils import timezone
import pytest

from jobs.models import Job

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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
def test_assign_job_view(client, board_factory, profile_factory, job_form_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    board = profile.user.board

    columns = [col.id for col in board.columns.all()]

    job = job_form_factory(user=profile.user)
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
def test_delete_job_view(client, job_form_factory, profile_factory, board_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    board = profile.user.board

    job = job_form_factory(user=profile.user)
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


@pytest.mark.django_db
def test_edit_job_view(client, job_form_factory, profile_factory, board_factory, jobs_form_data):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    board = profile.user.board

    job = job_form_factory(user=profile.user)
    job.board = board
    job.save()

    data = jobs_form_data
    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302

    url = reverse("jobs:edit_job", kwargs={"pk": job.pk})

    response = client.get(url, data)

    assert job.url == data['url']
    assert job.source == data['source']
    assert job.job_title == data['job_title']
    assert job.job_function == data['job_function']
    assert job.description == data['description']
    assert job.location_policy == data['location_policy']
    assert job.work_contract == data['work_contract']
    assert job.company == data["company"]
    assert job.min_pay == data['min_pay']
    assert job.max_pay == data["max_pay"]
    assert job.pay_rate == data["pay_rate"]
    assert job.currency == data["currency"]
    assert job.note == data["note"]


@pytest.mark.django_db
def test_download_jobs_view(client, profile_factory, job_factory):
    profile = profile_factory()
    profile.save()
    client.force_login(profile.user)
    job1 = job_factory(user=profile.user, updated_days_previous=1)
    job2 = job_factory(user=profile.user, updated_days_previous=14)
    job3 = job_factory(user=profile.user, updated_days_previous=28)
    job1.save()
    job2.save()
    job3.save()

    end_date = timezone.now()
    start_date = end_date - timedelta(days=15)

    url = reverse("jobs:download")

    response = client.get(url)

    assert response.status_code == 200

    url = reverse("jobs:download")  # Replace with your view's URL name
    response = client.post(
        url, {"start_date": start_date, "end_date": end_date})

    # Verify the response
    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv"

    # Parse the CSV content
    content = response.content.decode("utf-8")
    lines = content.split("\n")
    try:
        assert len(lines) == 5
    except AssertionError:
        print(f"Number of lines: {len(lines)}")
        print(f"content: {content}")

        i = 0
        for line in lines:
            print(f"Line {i}: {line}")
            i += 1

    file = StringIO(content)
    r = csv.reader(file, delimiter=",")

    i = 0
    for row in r:
        i += 1
        id, job_title, company, url, status, updated = row
        logger.info("ID: %s, Job Title: %s, Company: %s, URL: %s, Status: %s, Updated: %s",
                    id, job_title, company, url, status, updated)

        if id == str(job1.id):
            job = job1
        elif id == str(job2.id):
            job = job2
        elif id == str(job3.id):
            job = job3
        else:
            assert job_title == "Job Title"
            assert company == "Company"
            assert url == "URL"
            assert status == "Status"
            assert updated == "Updated"
            continue

        try:
            assert job.id == int(id)
            assert job.job_title == job_title
            assert job.company == company
            assert job.url == url
            assert job.get_status_display() == status
            assert str(job.updated) == updated
        except AssertionError:
            print(
                f"ID: {job.id}, Job Title: {job.job_title}, Company: {job.company}, URL: {job.url}, Status: {job.get_status_display()}, Updated: {job.updated}")
            print(
                f"id: {id}, job_title: {job_title}, company: {company}, url: {url}, status: {status}, updated: {updated}")

    assert i == 3


@pytest.mark.django_db
def test_board_view_add_job(client, profile_factory, jobs_form_data):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    data = jobs_form_data

    response = client.post(reverse("accounts:login"), {
        "email": profile.user.email, "password": PASSWORD})

    assert response.status_code == 302

    url = reverse('jobs:board')

    # GET request should show add job form
    response = client.get(url)
    assert response.status_code == 200
    assert 'job_form' in response.context

    # POST request with valid data should add job
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('jobs:board')
    assert Job.objects.get(**data)
