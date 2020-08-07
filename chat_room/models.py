from django.db import models
from django.conf import settings

# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)


class Message(models.Model):
    class Test(models.TextChoices):
        REQUEST = "request"
        REPLY = "reply"
    
    msg_type = models.CharField(
        choices = Test.choices, 
        max_length = 7,
    )

    text = models.TextField()
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date_sent = models.DateTimeField(auto_now_add=True)