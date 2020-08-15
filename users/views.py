from django.contrib.auth import views as auth_views, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import UserCreationForm

# Create your views here.
class LoginView(auth_views.LoginView):
    template_name = "users/login.html"

    extra_context = {}

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            user = authenticate(username=user.username, password=form.cleaned_data["password1"])
            login(request, user)

            return HttpResponseRedirect(reverse("lesson_planner:index"))

    else:
        form = UserCreationForm()

    context = {"form": form}

    return render(request, "users/sign_up.html", context)

def log_out(request):
    logout(request)

    return HttpResponseRedirect(reverse("lesson_planner:index"))
