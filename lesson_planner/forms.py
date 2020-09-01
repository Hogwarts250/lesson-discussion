from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Series, Lesson
from users.models import User


class SeriesForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        to_field_name=None,
    )
    students.widget.attrs.update({
        "class": "form-check"
    })

    start_datetime = forms.SplitDateTimeField(
        label="Start datetime",
        widget=forms.SplitDateTimeWidget(
            date_attrs={
                "class" : "form-control",
                "data-provide": "datepicker",
                "placeholder": "placeholder",
            },
            date_format="%d/%m/%Y",
            time_attrs={
                "class": "form-control",
                "placeholder": "placeholder",
            },
            time_format="%H:%M",
        )
    )
    end_date = forms.DateField(
        input_formats=["%d/%m/%Y"],
        label="End date",
        required=False,
    )
    end_date.widget.attrs.update({
        "class": "form-control",
        "data-provide": "datepicker",
        "placeholder": end_date.label,
    })

    class Meta:
        model = Series
        fields = ["name", "students", "amount", "start_datetime", "length", "repeat", "end_date"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "placeholder",
            }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "placeholder",
            }),
            "length": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "placeholder",
                },
            ),
                "repeat": forms.Select(attrs={
                "class": "form-control",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_datetime").date()
        end_date = cleaned_data.get("end_date")

        if (start_date and end_date) and (start_date >= end_date):
            raise ValidationError("Selected end date must be after the first lesson")

        repeat = cleaned_data.get("repeat")

        if repeat != Series.RepeatChoices.NEVER and end_date == None:
            raise ValidationError("An end date is required")

        return cleaned_data

class CreateSeriesForm(SeriesForm):
    def __init__(self, user_id, * args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["students"].queryset = User.objects.exclude(id=user_id)


class RequestSeriesForm(SeriesForm):
    teacher = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
    )
    teacher.widget.attrs.update({
        "class": "form-control",
    })

    class Meta(SeriesForm.Meta):
        fields = SeriesForm.Meta.fields
        fields.append("teacher")

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teacher"].queryset = User.objects.exclude(id=user_id)
        self.fields["students"].queryset = User.objects.all()

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("teacher") in cleaned_data.get("students"):
            raise ValidationError("The teacher cannot also be a student")

        return cleaned_data


class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["students", "datetime", "length"]
