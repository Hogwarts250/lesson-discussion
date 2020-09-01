import uuid
from model_utils import fields, Choices

from django.db import models
from django.conf import settings
from django.core import validators

from lesson_planner.models import Series

# Create your models here.
class TransactionRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)


class Transaction(models.Model):
    class SendRequestChoices(models.TextChoices):
        SEND = "send"
        REQUEST = "request"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="initial_sender",
        null=True,
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="initial_receiver",
        null=True
    )
    last_sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_by",
        null=True
    )
    transaction_record = models.ForeignKey(TransactionRecord, on_delete=models.CASCADE)

    send_request = models.CharField(
        choices=SendRequestChoices.choices,
        default=SendRequestChoices.REQUEST,
        max_length=7,
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[validators.MinValueValidator(0.01)],
        null=True
    )
    note = models.TextField(blank=True, default=None)

    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)

    STATUS = Choices("pending", "confirmed", "sent", "received", "denied")
    status = fields.StatusField(choices=STATUS, default=STATUS.pending, max_length=10)
    confirmed_datetime = fields.MonitorField(
        monitor="status",
        when=STATUS.confirmed,
        null=True
    )
    sent_datetime = fields.MonitorField(
        monitor="status",
        when=STATUS.sent,
        null=True
    )
    received_denied_datetime = fields.MonitorField(
        monitor="status",
        when=[STATUS.received, STATUS.denied],
        null=True
    )

    def set_status_confirmed(self, **kwargs):
        self.status = self.STATUS.confirmed
        self.save()

    def set_status_sent(self, **kwargs):
        self.status = self.STATUS.sent
        self.last_sent_by = kwargs["user"]
        self.save()

    def set_status_received(self, **kwargs):
        self.status = self.STATUS.received
        self.last_sent_by = kwargs["user"]
        self.save()

    def set_status_denied(self, **kwargs):
        self.status = self.STATUS.denied
        self.last_sent_by = kwargs["user"]
        self.save()

    def get_other_user(self, user):
        return self.receiver if user == self.sender else self.sender
