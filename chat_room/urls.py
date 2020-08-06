from django.contrib import admin
from django.urls import path

from . import views

appname = "chat_room"
urlpatterns = [
    path("", views.index, name="index"),
]