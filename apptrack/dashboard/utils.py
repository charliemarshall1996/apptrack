
def calculate_conversion_score(jobs):
    interviews = jobs.objects.filter(interviewed=True).count()
    applications = jobs.objects.filter(applied=True).count()
    offers = jobs.objects.filter(applied=True).count()

    return (interviews + (offers * 2) / applications)
