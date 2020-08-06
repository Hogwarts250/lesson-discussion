from django import forms
from django.contrib.auth import forms as auth_forms, models

# Create your forms here.
class SignUpForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    email = forms.EmailField()

    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]