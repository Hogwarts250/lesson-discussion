from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import User
from .forms import UserCreationForm, UserChangeForm

# Register your models here.
class UserAdmin(auth_admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
    ]

admin.site.register(User, UserAdmin)
