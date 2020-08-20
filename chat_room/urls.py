from django.contrib import admin
from django.urls import path

from . import views

app_name = "chat_room"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:other_id>/", views.room, name="room")
]