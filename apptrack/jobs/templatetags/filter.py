"""Custom template tag for filtering jobs by column."""
# filter.py

from django import template

register = template.Library()


@register.filter(name="column_jobs")
def comm_sheet(jobs, column):  # noqa: D103
    return jobs.filter(column=column)
