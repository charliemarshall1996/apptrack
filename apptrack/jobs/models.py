
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from accounts.models import Profile, Target
from core.models import Country, Currency

from .choices import (
    StatusChoices,
    SourceChoices,
    ReminderUnitChoices
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create your models here.


class Task(PolymorphicModel):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0, null=True, blank=True)


class TargetTask(Task):
    target = models.ForeignKey(
        Target, related_name="task", on_delete=models.CASCADE)

    @property
    def current_val(self):
        return self.target.current

    @property
    def target_val(self):
        return self.target.daily_target

    @property
    def type(self):
        return "target"

    def save(self, *args, **kwargs):
        if self.target.met:
            self.is_completed = True
        self.priority = 1
        super().save(*args, **kwargs)


class Feedback(PolymorphicModel):
    name = models.CharField(max_length=255)


class PositiveFeedback(Feedback):

    @property
    def type(self):
        return "positive"


class NegativeFeedback(Feedback):

    @property
    def type(self):
        return "negative"


class Board(models.Model):
    name = models.CharField(max_length=255, null=True,
                            blank=True, default="My Job Board")

    profile = models.OneToOneField(Profile,
                                   on_delete=models.CASCADE, related_name='board')


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


class JobFunction(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LocationPolicy(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PayRate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkContract(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(models.Model):

    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile,
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
    job_function = models.ForeignKey(
        JobFunction, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    company = models.CharField(max_length=100, null=True, blank=True)
    is_recruiter = models.BooleanField(default=False, null=True, blank=True)

    location_policy = models.ForeignKey(
        LocationPolicy, on_delete=models.SET_NULL, null=True, blank=True)
    work_contract = models.ForeignKey(
        WorkContract, on_delete=models.SET_NULL, null=True, blank=True
    )

    min_pay = models.IntegerField(null=True, blank=True)
    max_pay = models.IntegerField(null=True, blank=True)
    pay_rate = models.ForeignKey(
        PayRate, on_delete=models.SET_NULL, null=True, blank=True
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, blank=True
    )

    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )

    note = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=2, choices=StatusChoices.choices(), default=StatusChoices.default())

    applied = models.BooleanField(null=True, blank=True)
    date_applied = models.DateField(null=True, blank=True)
    interviewed = models.BooleanField(null=True, blank=True)
    date_interviewed_set = models.DateField(null=True, blank=True)
    archived = models.BooleanField(null=True, blank=True, default=False)
    auto_archive = models.BooleanField(null=True, blank=True, default=False)
    archive_after_weeks = models.IntegerField(null=True, blank=True, default=2)

    positive_feedback = models.ManyToManyField(
        PositiveFeedback, blank=True, null=True)
    negative_feedback = models.ManyToManyField(
        NegativeFeedback, blank=True, null=True)

    def __str__(self):
        return f"{self.company} - {self.job_title}"

    def _update_if_changed(self):
        if self.pk:
            logger.debug("PK exists")
            original = Job.objects.filter(pk=self.pk).first()
            if not original:
                logger.debug("Original does not exist")
                self.updated = timezone.now()
            else:
                logger.debug("Original exists")
                if original.status != self.status \
                        or original.note != self.note:
                    logger.debug("Status or note has changed")
                    logger.info("Updating job...")
                    self.updated = timezone.now()

    def _manage_columns_and_boards(self):
        logger.info("Managing columns and boards...")

        # Check if the column
        # is not already set
        if not self.column and self.board:
            self.board.save()
            try:
                position = StatusChoices.get_status_column_position(
                    self.status)
                name = StatusChoices.get_column_position_status_name(position)

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
                    f"Column with position {StatusChoices.get_status_column_position(self.status)} for board {self.board} does not exist.")

        elif self.column:
            logger.info("Column exists")
            self.board.save()
            self.column.board = self.board
            self.column.save()

            original = Job.objects.filter(pk=self.pk).first()

            if original and original.status != self.status:
                self.column = Column.objects.filter(
                    board=self.board, position=StatusChoices.get_status_column_position(self.status)).first()
            elif original and original.column != self.column:
                self.status = StatusChoices.get_column_position_status(
                    self.column.position
                )

    def _set_applied(self):
        logger.info("Setting applied...")
        if self.status in StatusChoices.get_applied_statuses():
            logger.info("Job is applied")
            self.applied = True
            if not self.date_applied:
                self.date_applied = timezone.now()
        else:
            if (self.status != StatusChoices.REJECTED)\
                    and (self.status != StatusChoices.CLOSED):
                logger.info("Job is not applied")
                self.applied = False
                self.profile.target.decrement()
                self.profile.target.save()

    def _set_interviewed(self):
        logger.info("Setting interviewed...")
        if self.status in [StatusChoices.INTERVIEW, StatusChoices.OFFER]:
            self.interviewed = True
            if not self.date_interviewed_set:
                self.date_interviewed_set = timezone.now()

    def _manage_profile_streak(self):
        profile_target = Target.objects.get(profile=self.profile)
        # if job is applied
        if self.applied:

            # if job was not previously applied
            try:
                original = Job.objects.get(pk=self.pk)
                if not original.applied:
                    print(
                        "Incrementing applications made, job changed to applied")
                    profile_target.increment()
                    profile_target.save()
            except Job.DoesNotExist:
                print("Incrementing applications made, job created with applied")
                profile_target.increment()
                profile_target.save()

    def save(self, *args, **kwargs):
        self._manage_columns_and_boards()
        # Call the parent's save method to persist the object

        self._update_if_changed()

        self._set_applied()
        self._set_interviewed()
        self._manage_profile_streak()
        super().save(*args, **kwargs)


# Create your models here.
class Reminder(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    offset = models.IntegerField(default=1)
    unit = models.CharField(
        max_length=1, choices=ReminderUnitChoices.choices())

    emailed = models.BooleanField(default=False, blank=True)
    read = models.BooleanField(default=False)


class Interview(models.Model):
    interview_round = models.IntegerField(default=1)

    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='interviews')
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    post_code = models.CharField(max_length=10, blank=True, null=True)
    building = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    region = models.CharField(max_length=20, blank=True, null=True)
    meeting_url = models.URLField(blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.job.job_title} at {self.job.company}"

    def create_default_tasks(self):
        default_tasks = [
            "Prepare for interview",
            "Review job description",
            "Research the company",
            "Prepare questions for the interviewer",
            "Dress appropriately",
            "Plan your route to the interview",
        ]
        for task in default_tasks:
            InterviewTask.objects.create(
                interview=self, profile=self.profile, name=task)

    def save(self, *args, **kwargs):
        if not self.pk:  # This ensures tasks are added only once when the interview is created
            super().save(*args, **kwargs)
            self.create_default_tasks()
        else:
            super().save(*args, **kwargs)


class InterviewReminder(Reminder):
    interview = models.ForeignKey(
        Interview, on_delete=models.CASCADE, related_name='reminders')

    @property
    def message(self):
        return f"Reminder: Interview for {self.interview.job.job_title} at {self.interview.job.company} in {self.alert_before} {self.alert_before_unit}"


class InterviewTask(Task):
    interview = models.ForeignKey(
        Interview, related_name="tasks", on_delete=models.CASCADE)

    @property
    def type(self):
        return "interview"

    def save(self, *args, **kwargs):
        self.priority = 2
        super().save(*args, **kwargs)


class JobTask(Task):
    job = models.ForeignKey(
        Job, related_name="tasks", on_delete=models.CASCADE)

    @property
    def type(self):
        return "job"

    def save(self, *args, **kwargs):
        self.priority = 3
        super().save(*args, **kwargs)
