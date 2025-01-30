from jobs.models import Job
from company.models import Company


def run():
    for job in Job.objects.all():

        company, created = Company.objects.get_or_create(
            profile=job.profile, name=job.company)
        if created:
            company.profile = job.profile
            company.save()
