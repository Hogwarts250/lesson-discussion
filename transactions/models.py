import uuid

from django.db import models
from django.conf import settings

from model_utils import fields, Choices

# Create your models here.
class TransactionRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="buyer",
        null=True,
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller",
        null=True
    )
    last_sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_by",
        null=True
    )
    transaction_record = models.ForeignKey(
        TransactionRecord, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)

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

    def get_other_user(self, user):
        return self.seller if user == self.buyer else self.buyer
