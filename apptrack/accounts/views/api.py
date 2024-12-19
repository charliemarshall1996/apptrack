from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.models import Job
from target.models import Target

from accounts.models import Profile
from .utils import ConversionCalculator

User = get_user_model()


class ProfileAPI(APIView):
    def get(self, request, id):
        """
        Handles GET requests to the API for a given user.

        This function gets the data for a given user and
        returns it as a JSON response.

        Args:
            - :param request: The HTTP request object
            - :param id: The id of the user whose data is being requested

        Returns:
            - :return: A Response object containing the JSON data
        """
        user = User(id=id)
        profile = Profile.objects.get(user=user)

        data = {
            "basic_stats": self._get_basic_stats(profile),
            "streak": self._get_user_streak(profile),
        }

        return Response(data)

    def _get_user_streak(self, profile):
        """
        Retrieves the user's current application target and streak information.

        This method attempts to fetch the Target object associated with the user's
        profile. If no Target exists, a new one is created and saved. It then collects
        the current number of applications and the current streak from the Target.

        Args:
            - profile (`Profile`): The Profile object representing the user's profile.

        Returns:
            - `dict`: A dictionary containing the current application target, current
            streak, and formatted display strings for the target and streak.
        """

        # Retrieve the Target object
        # associated with the user's profile
        try:
            target = Target.objects.get(profile=profile)
        except Target.DoesNotExist:
            target = Target(profile=profile)
            target.save()

        # Collect the current number of applications
        # and the current streak
        current_applications = target.current
        streak = target.streak.current_streak

        return {
            "target": target.amount,
            "current_applications": current_applications,
            "streak": streak,
            "target_display": f"Application Target: {current_applications}/{target.amount}",
            "streak_display": f"Current Streak: {streak} Days",
        }

    def _get_basic_stats(self, profile):
        """
        Retrieves basic statistics related to job applications for a given user profile.

        This method calculates various statistics such as the total number of jobs,
        active jobs, applied jobs, interviewed jobs, and offers associated with the
        user's profile. Additionally, it computes conversion rates and scores using
        these statistics.

        Args:
            - profile (`Profile`): The Profile object representing the user's profile.

        Returns:
            - `dict`: A dictionary containing the following keys and their respective values:
                - `total_jobs`: Total number of jobs associated with the profile.
                - `total_active_jobs`: Total number of active (non-archived) jobs.
                - `total_applied_jobs`: Total number of jobs the user has applied to.
                - `total_interviewed_jobs`: Total number of jobs for which the user has been interviewed.
                - `total_offers`: Total number of job offers received.
                - `total_active_interviews`: Total number of active interviews.
                - `total_active_offers`: Total number of active offers.
                - `conversion_score`: Conversion score calculated based on applications, interviews, and offers.
                - `conversion_rate`: Conversion rate from applications to offers.
                - `interview_conversion_rate`: Conversion rate from applications to interviews.
                - `offer_conversion_rate`: Conversion rate from applications to offers.
        """

        total_jobs = Job.objects.filter(profile=profile).count()
        total_active_jobs = Job.objects.filter(profile=profile, archived=False).count()
        total_applied_jobs = Job.objects.filter(profile=profile, applied=True).count()
        total_interviewed_jobs = Job.objects.filter(
            profile=profile, interviewed=True
        ).count()
        total_active_interviews = Job.objects.filter(
            profile=profile, interviewed=True, archived=False
        ).count()
        total_active_offers = Job.objects.filter(
            profile=profile, offered=True, archived=False
        ).count()
        total_offers = Job.objects.filter(profile=profile).count()

        return {
            "total_jobs": total_jobs,
            "total_applied_jobs": total_applied_jobs,
            "total_interviewed_jobs": total_interviewed_jobs,
            "total_offers": total_offers,
            "total_active_jobs": total_active_jobs,
            "total_active_interviews": total_active_interviews,
            "total_active_offers": total_active_offers,
            "conversion_score": ConversionCalculator.calculate_conversion_score(
                total_applied_jobs, total_interviewed_jobs, total_offers
            ),
            "conversion_rate": ConversionCalculator.calculate_conversion_rate(
                total_applied_jobs, total_interviewed_jobs, total_offers
            ),
            "interview_conversion_rate": ConversionCalculator.calculate_basic_conversion_rate(
                total_applied_jobs, total_interviewed_jobs
            ),
            "offer_conversion_rate": ConversionCalculator.calculate_basic_conversion_rate(
                total_applied_jobs, total_offers
            ),
        }


"""
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July'
        ]
        chartLabel = "my data"
        chartdata = [0, 10, 5, 2, 20, 30, 45]
        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": chartdata,
        }
        return Response(data)
"""
