from django.contrib.auth import views as auth_views, login, authenticate, logout
from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.http import HttpResponseRedirect
# from django.urls import reverse

# from .forms import SignUpForm

# Create your views here.
class LoginView(auth_views.LoginView):
    pass

def sign_up(request):
    pass

    # if request.method == "POST":
    #     form = SignUpForm(request.POST)

    #     if form.is_valid():
    #         user = form.save()
    #         user.refresh_from_db()
    #         user.username = form.cleaned_data["email"]
    #         user.save()

    #         user = authenticate(username=user.username, password=form.cleaned_data["password1"])
    #         login(request, user)

    #         return HttpResponseRedirect(reverse("lesson_planner:index"))

    # else:
    #     form = SignUpForm()

    # return render(request, "users/sign_up.html", context)

@login_required
def log_out(request):
    pass

    # logout(request)

    # return HttpResponseRedirect(reverse("lesson_planner:index"))
