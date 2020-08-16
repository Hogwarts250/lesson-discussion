from django import forms
from django.conf import settings

from .models import Lesson
from users.models import User

class LessonForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset = None,
        to_field_name = None,
        widget = forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Lesson
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["students"].queryset = User.objects.all()
