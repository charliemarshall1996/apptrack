"""This module processes the job download view.

Manages the job download view for the requesting user. Allowing them to download a CSV 
file of their jobs based on a provided date range.
"""

import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from jobs.forms import DownloadJobsForm
from jobs.models import Job


@login_required
def job_download_view(request):
    """Manages the job download view for the requesting user.

    Allows the user to download a CSV file of their jobs based on a provided date range.
    If the request method is GET, it renders a form for the user to input the date 
    range. If the request method is POST, it generates a CSV file with the jobs in the 
    specified date range and returns it as a response.

    The CSV file will have the following columns: ID, Job Title, Company, URL, Status,
    and Updated.

    Args:
        request: The current request

    Returns:
        HttpResponse: A CSV file with the jobs in the specified date range if the 
            request method is POST, or a form for the user to input the date range if 
                the request method is GET
    """
    if request.method == "GET":
        form = DownloadJobsForm()
        return render(
            request,
            "jobs/download_jobs.html",
            {"form": form, "user_id": request.user.id},
        )

    # Handle POST request (CSV file generation)
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    # Filter jobs based on the `updated` field
    jobs = Job.objects.filter(updated__range=(
        start_date, end_date)).order_by("id")

    filename = f"jobs_{start_date}_{end_date}.csv"
    # Prepare the response
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

    # Write the CSV file
    writer = csv.writer(response)
    writer.writerow(
        ["ID", "Job Title", "Company", "URL", "Status", "Updated"]
    )  # CSV headers

    for job in jobs:
        writer.writerow(
            [
                job.id,
                job.job_title,
                job.company,
                job.url,
                job.get_status_display(),
                job.updated,
            ]
        )

    return response
