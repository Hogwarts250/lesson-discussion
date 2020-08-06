from django.contrib import admin
from django.urls import path

from . import views

appname = "lesson_planner"
urlpatterns = [
    path("", views.index, name="index"),
]