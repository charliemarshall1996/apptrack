# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Employee

# ...


def home(request):
    employees = Employee.objects.all()
    task = Task.objects.all()
    spare_task = Task.objects.filter(employee__isnull=True)

    context = {'employees': employees,
               'tasks': task,
               'spare_tasks': spare_task}
    return render(request, 'kanban/assign_sheets.html', context)


class ChangeSheetAssign(View):

    @staticmethod
    def get(request, *args, **kwargs):
        emp_id = kwargs['emp_id']
        task_id = kwargs['task_id']

        employee = Employee.objects.get(id=emp_id)
        task = Task.objects.get(id=task_id)

        employee.task = task
        task.save()

        return redirect(reverse('kanban:home'))

# render page


class AssignTask(View):

    @staticmethod
    def get(request, *args, **kwargs):
        employees = Employee.objects.all()
        task = Task.objects.all()

        context = {'employees': employees,
                   'tasks': task}

        return render(request, 'kanban/assign_sheets.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        emp_id = kwargs['emp_id']
        task_id = kwargs['task_id']

        employee = Employee.objects.get(id=emp_id)
        task = Task.objects.get(id=task_id)

        task.employee = employee
        task.save()

        return redirect(reverse('kanban:home'))
