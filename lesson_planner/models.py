import uuid

from django.db import models
from django.conf import settings

from model_utils import fields, Choices

# Create your models here.
class Lesson(models.Model):
    class RepeatChoices(models.TextChoices):
        NEVER = "never"
        DAILY = "daily"
        WEEKLY = "weekly"
        MONTHLY = "monthly"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    label = models.CharField(max_length=50, null=True)

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "teacher", 
        null = True,
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name = "students", 
        blank = True,
    )

    repeat = models.CharField(
        choices = RepeatChoices.choices, 
        default = RepeatChoices.NEVER,
        max_length = 7,
    )

    length = models.DurationField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    date = models.DateField()

    datetime_created = models.DateTimeField(auto_now_add=True)