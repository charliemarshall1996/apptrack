
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from core.models import Task

from .choices import (
    CurrencyChoices,
    CountryChoices,
    JobFunctionChoices,
    LocationPolicyChoices,
    WorkContractChoices,
    PayRateChoices,
    StatusChoices,
    SourceChoices,
)


User = get_user_model()


# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=255, null=True,
                            blank=True, default="My Job Board")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='board')

    def save(self, *args, **kwargs):
        if not self.name or self.name == 'None':
            self.name = "My Job Board"

        super().save(*args, **kwargs)

        default_columns = [
            ('Open', 1),
            ('Applied', 2),
            ('Shortlisted', 3),
            ('Interview', 4),
            ('Offer', 5),
            ('Rejected', 6),
            ('Closed', 7),
        ]

        for name, position in default_columns:
            if not Column.objects.filter(name=name, board=self).exists():
                column = Column(name=name, position=position, board=self)
                column.save()
                print(f"Column added: {column.name}")

        if not self.columns.exists():
            columns_to_add = Column.objects.all()
            self.columns.add(*columns_to_add)
            print(f"Columns added: {columns_to_add}")


class Column(models.Model):
    board = models.ForeignKey(
        'Board', on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255)
    position = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']
        unique_together = ('board', 'name', 'position')


class JobTask(Task):
    job = models.ForeignKey(
        'Job', on_delete=models.CASCADE, related_name='tasks')


class Job(models.Model):

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    column = models.ForeignKey(
        Column, related_name="column", on_delete=models.CASCADE, null=True, blank=True)
    board = models.ForeignKey(
        Board, related_name="jobs", on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    url = models.URLField(blank=True, null=True)
    source = models.CharField(
        max_length=2, choices=SourceChoices.choices(), null=True, blank=True)

    job_title = models.CharField(max_length=100, blank=True, null=True)
    job_function = models.CharField(
        max_length=2, choices=JobFunctionChoices.choices(), null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    company = models.CharField(max_length=100, null=True, blank=True)
    is_recruiter = models.BooleanField(default=False, null=True, blank=True)

    location_policy = models.CharField(
        max_length=100, choices=LocationPolicyChoices.choices(), null=True, blank=True)
    work_contract = models.CharField(
        max_length=100, choices=WorkContractChoices.choices(), null=True, blank=True)

    min_pay = models.IntegerField(null=True, blank=True)
    max_pay = models.IntegerField(null=True, blank=True)
    pay_rate = models.CharField(
        max_length=2, choices=PayRateChoices.choices(), null=True, blank=True)
    currency = models.CharField(
        max_length=3, null=True, blank=True, choices=CurrencyChoices.choices())

    town = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(
        max_length=2, choices=CountryChoices.choices(), null=True, blank=True)

    note = models.TextField(null=True, blank=True)
    print(StatusChoices.choices())
    status = models.CharField(
        max_length=2, choices=StatusChoices.choices(), default=StatusChoices.default())

    applied = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.job_title}"

    def _update_if_changed(self):
        if self.pk:
            original = Job.objects.filter(pk=self.pk).first()
            if original and original.status != self.status:
                self.updated = timezone.now()  # Update timestamp if status changes
            elif original and original.note != self.note:
                self.note = original.note
            else:
                self.updated = timezone.now()

    def _create_default_tasks(self):

        if self.status == StatusChoices.OPEN:
            default_tasks = [
                "Prepare for interview",
                "Review job description",
                "Research the company",
                "Prepare questions for the interviewer",
                "Dress appropriately",
                "Plan your route to the interview",
            ]
        elif self.status == StatusChoices.APPLIED:
            pass
        elif self.status == StatusChoices.SHORTLISTED:
            pass
        elif self.status == StatusChoices.INTERVIEW:
            default_tasks = ["Create Interview Event"]
        elif self.status == StatusChoices.OFFER:
            pass
        elif self.status == StatusChoices.REJECTED:
            pass
        for task in default_tasks:
            JobTask.objects.create(interview=self, name=task)

    def _manage_columns_and_boards(self):
        # If the board is not set,
        # set it to the column's board
        if not self.board and self.column:
            self.board = self.column.board

        try:
            if not self.column.board:
                self.column.board = self.board
        except AttributeError:
            pass

        # Check if the column
        # is not already set
        if not self.column and self.board:
            try:
                position = StatusChoices.get_status_column(self.status)
                name = StatusChoices.get_column_name(position)

                # Retrieve the correct column
                # based on the position and board
                col, created = Column.objects.get_or_create(
                    name=name,
                    position=position,
                    board=self.board
                )

                if created:
                    col.save()
                self.column = col
            except ObjectDoesNotExist:
                raise ValueError(
                    f"Column with position {StatusChoices.get_status_column(self.status)} for board {self.board} does not exist.")

        elif self.column:
            self.column.board = self.board
            # Ensure status is updated based on column position
            self.status = StatusChoices.get_column_status(self.column.position)
            self.column.save()

    def _set_applied(self):
        if self.status in StatusChoices.get_applied_statuses():
            self.applied = True
        else:
            self.applied = False

    def save(self, *args, **kwargs):

        self._update_if_changed()

        self._manage_columns_and_boards()

        self._set_applied()

        # Call the parent's save method to persist the object
        super().save(*args, **kwargs)
