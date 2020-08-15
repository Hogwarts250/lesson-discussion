from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name = "users"
urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("log-out/", views.log_out, name="log_out"),
]