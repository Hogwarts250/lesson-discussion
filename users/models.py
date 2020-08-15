from django.db import models
from django.contrib.auth import models as auth_models
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid

# Create your models here.
class User(auth_models.AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
