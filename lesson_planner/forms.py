from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Lesson
from users.models import User


class LessonForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        to_field_name=None,
    )

    lesson_datetime = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
    )
    end_date = forms.DateField(
        input_formats=["%d/%m/%Y"],
        required=False,
    )
    
    class Meta:
        model = Lesson
        exclude = ["transactions", "student_status", "confirmed_denied_datetime", "teacher"]

    def __init__(self, user_id, * args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["students"].queryset = User.objects.exclude(id=user_id)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("lesson_datetime").date()
        end_date = cleaned_data.get("end_date")

        if (start_date and end_date) and (start_date >= end_date):
            raise ValidationError("Chosen end date must be after the first lesson")

        repeat = cleaned_data.get("repeat")

        if repeat != Lesson.RepeatChoices.NEVER and end_date == None:
            raise ValidationError("An end date is required")


class RequestLessonForm(LessonForm):
    teacher = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
    )

    class Meta(LessonForm.Meta):
        exclude = ["transactions", "student_status", "confirmed_denied_datetime"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teacher"].queryset = User.objects.all()
        self.fields["students"].queryset = User.objects.all()
