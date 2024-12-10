
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

from jobs.models import Job, JobFunction, SourceChoices

from .utils import calculate_conversion_score


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


class BestConvertingJobFunctions(APIView):

    def get(self, request, id):
        conversion_scores = []
        labels = []
        chartLabel = "Best Converting Job Functions"
        for job_function in JobFunction.objects.all():
            jobs = Job.objects.filter(user=id, job_function=job_function)
            conversion_score = calculate_conversion_score(jobs)
            conversion_scores.append(conversion_score)
            labels.append(job_function.name)

        data = {
            "labels": labels,
            "chartData": conversion_scores,
            "chartLabel": chartLabel
        }
        return Response(data)


class BestConvertingSource(APIView):

    def get(self, request, id):
        conversion_scores = []
        labels = []
        chartLabel = "Best Converting Sources"
        for code, source in SourceChoices.choices():
            jobs = Job.objects.filter(user=id, source=code)
            conversion_score = calculate_conversion_score(jobs)
            conversion_scores.append(conversion_score)
            labels.append(source)

        data = {
            "labels": labels,
            "chartData": conversion_scores,
            "chartLabel": chartLabel
        }


class BestConvertingIndustries(APIView):

    def get(self, request, id):
        pass


class BestConvertingLocations(APIView):

    def get(self, request, id):
        pass
