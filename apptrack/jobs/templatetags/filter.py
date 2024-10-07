# filter.py

from django import template

register = template.Library()


@register.filter(name='column_jobs')
def comm_sheet(jobs, column):
    return jobs.filter(column=column)
