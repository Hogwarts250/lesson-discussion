import uuid
from model_utils import fields, Choices

from django.db import models
from django.conf import settings

# Create your models here.
class Series(models.Model):
    class StatusChoices(models.TextChoices):
        REQUEST = "request"
        CREATE = "create"
        DENIED = "denied"

    class RepeatChoices(models.TextChoices):
        NEVER = "never"
        DAILY = "daily"
        WEEKLY = "weekly"
        MONTHLY = "monthly"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.CREATE,
        max_length=7,
    )

    name = models.CharField(max_length=50, null=True)

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="series_teacher",
        null=True,
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="series_students",
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    length = models.DurationField(null=True)

    repeat = models.CharField(
        choices=RepeatChoices.choices,
        default=RepeatChoices.NEVER,
        max_length=7,
    )
    # start and end dates are inclusive
    start_datetime = models.DateTimeField(null=True)
    end_date = models.DateField(null=True, blank=True)

    def set_status_confirmed(self):
        self.status = self.StatusChoices.CREATE
        self.save()

    def set_status_denied(self):
        self.status = self.StatusChoices.DENIED
        self.save()


class Lesson(models.Model):
    class StatusChoices(models.TextChoices):
        REQUEST = "request"
        CREATE = "create"
        DENIED = "denied"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.CREATE,
        max_length=7,
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_teacher",
        null=True,
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="lesson_students",
    )

    datetime = models.DateTimeField(null=True)


class StudentStatus(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)

    STATUS = Choices("pending", "confirmed", "denied")
    status = fields.StatusField(
        choices=STATUS, default=STATUS.pending, max_length=10)

    confirmed_denied_datetime = fields.MonitorField(
        monitor="status",
        when=[STATUS.confirmed, STATUS.denied],
        null=True
    )

    def set_status_confirmed(self):
        self.status = self.STATUS.confirmed
        self.save()

    def set_status_denied(self):
        self.status = self.STATUS.denied
        self.save()
