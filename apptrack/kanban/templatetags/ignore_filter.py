# filter.py

from django import template

register = template.Library()


@register.filter(name='employee_tasks')
def comm_sheet(tasks, employee):
    return tasks.filter(employee=employee)
