from django.contrib import admin
from django.urls import path

from . import views

app_name = "lesson_planner"
urlpatterns = [
    path("", views.index, name="index"),
    path("m=<str:model_id>", views.index, name="index"),
    path("create/", views.create_lesson, name="create_lesson"),
    path("request/", views.request_lesson, name="request_lesson"),
]
