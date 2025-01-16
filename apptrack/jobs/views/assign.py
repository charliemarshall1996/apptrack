"""Manages the assignment of jobs to columns. In the job board view."""
import logging

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.models import Column, Job

logger = logging.getLogger(__name__)

User = get_user_model()


class JobAssignView(APIView):
    """Manages the assignment of jobs to columns.

    This class view manages the assignment of jobs to columns in the job board view.
    It handles POST requests. APIView is used to provide a Response object.
    """

    def post(self, request, *args, **kwargs):
        """Handles POST requests for the assignment of a job to a column.

        This function manages the assignment of a job to a column in the job board view.
        It handles POST requests and assigns the job to the column specified by the
        url parameter 'col_id' and the job specified by the url parameter 'job_id'.

        Args:
            request (HttpRequest): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
                'col_id' (int): The ID of the column to assign the job to.
                'job_id' (int): The ID of the job to assign to the column.

        Returns:
            Response: The response object.
        """
        logger.debug("Assigning job...")
        col_id = kwargs["col_id"]
        job_id = kwargs["job_id"]

        column = Column.objects.get(id=col_id)
        job = Job.objects.get(id=job_id)

        job.column = column
        logger.debug("Job assigned to column %s", column)

        job.save()
        column.save()
        logger.debug("Job saved successfully to column: %s", column)

        data = {"job_status": job.status, "job_id": job.id}
        return Response(data)
