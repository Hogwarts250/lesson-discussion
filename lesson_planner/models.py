from django.db import models
from django.conf import settings

# Create your models here.
class Lesson(models.Model):
    class RepeatOptions(models.TextChoices):
        NEVER = "never"
        DAILY = "daily"
        WEEKLY = "weekly"
        MONTHLY = "monthly"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="students", blank=True)
    repeat = models.CharField(
        choices = RepeatOptions.choices, 
        default = RepeatOptions.NEVER,
        max_length = 7,
    )

    length = models.DurationField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    date = models.DateField()