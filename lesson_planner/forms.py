from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Lesson, Series
from users.models import User

class SeriesForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
    )
    end_date = forms.DateField(
        input_formats=["%d/%m/%Y"],
        required=False,
    )

    class Meta:
        model = Series
        fields = ["amount", "start_datetime", "length", "repeat", "end_date"]

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_datetime").date()
        end_date = cleaned_data.get("end_date")

        if (start_date and end_date) and (start_date >= end_date):
            raise ValidationError("Selected end date must be after the first lesson")

        repeat = cleaned_data.get("repeat")

        if repeat != Series.RepeatChoices.NEVER and end_date == None:
            raise ValidationError("An end date is required")


class LessonForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        to_field_name=None,
    )

    class Meta:
        model = Lesson
        exclude = ["datetime_created", "status", "series", "datetime"]


class CreateLessonForm(LessonForm):    
    class Meta(LessonForm.Meta):
        exclude = ["datetime_created", "status", "series", "teacher", "datetime"]

    def __init__(self, user_id, * args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["students"].queryset = User.objects.exclude(id=user_id)


class RequestLessonForm(LessonForm):
    teacher = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
    )

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teacher"].queryset = User.objects.exclude(id=user_id)
        self.fields["students"].queryset = User.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        teacher = cleaned_data.get("teacher")
        students = cleaned_data.get("students")

        if teacher in students:
            raise ValidationError("The teacher cannot also be a student")

        return cleaned_data
