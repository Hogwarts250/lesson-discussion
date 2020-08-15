from django import forms
from django.contrib.auth import forms as auth_forms
from django.conf import settings

from .models import User

# Create your forms here.
class UserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )

class UserChangeForm(auth_forms.UserChangeForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )