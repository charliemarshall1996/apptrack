"""Manages the provision of interview details."""
from django.http import JsonResponse
from jobs.models import Interview

# TODO: Make this a class-based APIview


def interview_detail_view(request, interview_id):
    """Provides the details of an interview as JSON.

    Args:
        request: The request object.
        interview_id: The ID of the interview to retrieve.

    Returns:
        A JSON response containing the interview details if the interview is found,
        otherwise a 404 response with an error message.
    """
    try:
        interview = Interview.objects.get(id=interview_id)
        print(interview.start_date.isoformat())

        interview_reminders = [
            {"id": r.id, "offset": r.offset, "unit": r.unit}
            for r in interview.reminders.all()
        ]

        interview_tasks = [
            {"id": task.id, "name": task.name, "completed": task.is_completed}
            for task in interview.tasks.all()
        ]
        # Return interview data as JSON
        response_data = {
            "id": interview.id,
            "title": interview.job.job_title,
            "company": interview.job.company,
            # Just the date part (YYYY-MM-DD)
            "date": interview.start_date.date().isoformat(),
            # Start time (HH:MM)
            "start_time": interview.start_date.strftime("%H:%M"),
            # End time (HH:MM)
            "end_time": interview.end_date.strftime("%H:%M"),
            "notes": interview.notes,
            "tasks": interview_tasks,
            "reminders": interview_reminders,
        }
        print(response_data)
        return JsonResponse(response_data)
    except Interview.DoesNotExist:
        return JsonResponse({"error": "Interview not found"}, status=404)
