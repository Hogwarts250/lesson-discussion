from django.db import models
from django.contrib.auth import models as auth_models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(auth_models.AbstractUser):
    pass

class TransactionRecord(models.Model):
    users = models.ManyToManyField(User, blank=True)

class Transaction(models.Model):
    transaction_record = models.ForeignKey(TransactionRecord, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)