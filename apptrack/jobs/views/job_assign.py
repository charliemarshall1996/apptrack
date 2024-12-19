import logging

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.models import Column, Job

logger = logging.getLogger(__name__)

User = get_user_model()


class JobAssignView(APIView):
    def post(request, *args, **kwargs):
        logger.debug("Assigning job...")
        col_id = kwargs["col_id"]
        job_id = kwargs["job_id"]

        print(f"col_id: {col_id}, job_id: {job_id}")
        column = Column.objects.get(id=col_id)
        job = Job.objects.get(id=job_id)

        print(f"column: {column}, job: {job}")
        job.column = column
        logger.debug("Job assigned to column %s", column)

        try:
            job.save()
            column.save()
            logger.debug("Job assigned successfully to column: %s", column)
        except Exception as e:
            logger.error("Error: %s", e)
        data = {"job_status": job.status, "job_id": job.id}
        return Response(data)
