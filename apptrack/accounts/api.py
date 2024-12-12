
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.models import (Job, JobFunction, Target)

from .models import Profile
from .utils import ConversionCalculator


class ProfileAPI(APIView):

    def get(self, request, id):

        profile = Profile.objects.get(id=id)

        data = {
            'basic_stats': self._get_basic_stats(profile),
            'streak': self._get_user_streak(profile),
        }

        return Response(data)

    def _get_user_streak(self, profile):
        target = Target.objects.get(profile=profile)
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

        total_jobs = Job.objects.filter(profile=profile).count()
        total_active_jobs = Job.objects.filter(
            profile=profile, archived=False).count()
        total_applied_jobs = Job.objects.filter(
            profile=profile, applied=True).count()
        total_interviewed_jobs = Job.objects.filter(
            profile=profile, interviewed=True).count()
        total_active_interviews = Job.objects.filter(
            profile=profile, interviewed=True, archived=False).count()
        total_active_offers = Job.objects.filter(
            profile=profile, offers=True, archived=False).count()
        total_offers = Job.objects.filter(profile=profile).count()

        return {'total_jobs': total_jobs,
                'total_applied_jobs': total_applied_jobs,
                'total_interviewed_jobs': total_interviewed_jobs,
                'total_offers': total_offers,

                'total_active_jobs': total_active_jobs,
                'total_active_interviews': total_active_interviews,
                'total_active_offers': total_active_offers,

                'conversion_score': ConversionCalculator.calculate_conversion_score(
                    total_applied_jobs, total_interviewed_jobs, total_offers
                ),
                'conversion_rate': ConversionCalculator.calculate_conversion_rate(
                    total_applied_jobs, total_interviewed_jobs, total_offers),
                'interview_conversion_rate': ConversionCalculator.calculate_basic_conversion_rate(total_applied_jobs, total_interviewed_jobs),
                'offer_conversion_rate': ConversionCalculator.calculate_basic_conversion_rate(total_applied_jobs, total_offers)}


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
