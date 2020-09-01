from django.contrib import admin
from django.urls import path

from . import views

app_name = "lesson_planner"
urlpatterns = [
    path("", views.index, name="index"),
    path("m=<str:model_id>", views.index, name="index"),
    path("create/", views.create_series, name="create_series"),
    path("request/", views.request_series, name="request_series"),
    path("edit/m=<str:series_id>", views.edit_series, name="edit_series"),
    path("edit/m=<str:lesson_id>", views.edit_lesson, name="edit_lesson"),
]
