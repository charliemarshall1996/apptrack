
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

from jobs.models import Job


def home_view(request):
    context = {"user_id": request.user.id}
    return render(request, "dashboard/dashboard.html", context)


class TotalApplications(APIView):

    def get(self, request, id):
        return Job.objects.filter(user=id, applied=True).count()


class BasicStats(APIView):

    def get(self, request, id):

        total_applied_jobs = Job.objects.filter(user=id, applied=True).count()
        total_interviews = Job.objects.filter(
            user=id, interviewed=True).count()

        if total_applied_jobs == 0 or total_interviews == 0:
            conversion_rate = 0
        else:
            conversion_rate = total_applied_jobs/total_interviews

        data = {
            "total_applications": total_applied_jobs,
            "total_interviews": total_interviews,
            "interview_conversion_rate": conversion_rate
        }

        return Response(data)


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
