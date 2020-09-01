from django.contrib import admin
from django.urls import path

from . import views

app_name = "transactions"
urlpatterns = [
    path("", views.index, name="index"),
    path("t=<str:transaction_id>", views.index, name="index"),
    path("create/", views.create_transaction, name="create_transaction"),
    path("edit/<str:transaction_id>/", views.edit_transaction, name="edit_transaction")
]
