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

    label = models.CharField(max_length=50, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name = "user", 
        on_delete = models.CASCADE,
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

class TransactionRecord(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

class Transaction(models.Model):
    STATUS = Choices("pending", "confirmed", "denied")

    def set_status_confirmed(self):
        self.status = STATUS.confirmed

    def set_status_denied(self):
        self.status = STATUS.denied

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name = "buyer", 
        on_delete = models.CASCADE,
        null = True,
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name = "seller", 
        on_delete = models.CASCADE,
        null = True
    )
    transaction_record = models.ForeignKey(TransactionRecord, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    status = fields.StatusField(choices=STATUS, default=STATUS.pending, max_length=10)
    date_sent = models.DateTimeField(auto_now_add=True)
    confirmed_denied_datetime = fields.MonitorField(
        monitor = "status", 
        when = [STATUS.confirmed, STATUS.denied],
        null = True
    )
