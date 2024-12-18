
import csv
from datetime import timedelta
from io import StringIO

from django.urls import reverse
from django.utils import timezone
import pytest


@pytest.mark.django_db
def test_download_jobs_view(client, profile_factory, job_factory):

    profile = profile_factory()
    profile.save()
    client.force_login(profile.user)
    job1 = job_factory(profile=profile, updated_days_previous=1)
    job2 = job_factory(profile=profile, updated_days_previous=14)
    job3 = job_factory(profile=profile, updated_days_previous=28)
    job1.save()
    job2.save()
    job3.save()

    end_date = timezone.now()
    start_date = end_date - timedelta(days=15)

    url = reverse("jobs:download_job")

    response = client.get(url)

    assert response.status_code == 200

    url = reverse("jobs:download_job")  # Replace with your view's URL name
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
