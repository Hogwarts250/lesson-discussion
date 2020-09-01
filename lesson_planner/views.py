from datetime import datetime, timedelta
from dateutil import relativedelta

from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.utils import timezone

from .models import Series, Lesson, StudentStatus
from .forms import CreateSeriesForm, RequestSeriesForm
from transactions.models import Transaction
from transactions.views import get_create_transaction_record, confirm_deny_model
from users.models import User

# Create your views here.
@login_required
def index(request, model_id=None):
    current_user = request.user
    series = Series.objects.filter(
        Q(teacher=current_user) | Q(students=current_user)
    ).distinct()
    requested_series = series.filter(status=Series.StatusChoices.REQUEST).order_by("start_datetime")
    created_series = series.filter(status=Series.StatusChoices.CREATE).order_by("start_datetime")

    if request.method == "POST":
        post_keys = "".join([k for k in request.POST.keys() if k != "csrfmiddlewaretoken"])
        if "series" in post_keys:
            series = series.get(id=model_id)
            confirm_deny_model(request, series)

        return HttpResponseRedirect(reverse("lesson_planner:index"))

    context = {"requested_series": requested_series, "created_series": created_series}

    return render(request, "lesson_planner/index.html", context)


@login_required
def create_series(request):
    current_user = request.user

    if request.method == "POST":
        form = CreateSeriesForm(current_user.id, data=request.POST)

        if form.is_valid():
            series = form.save()
            series.start_datetime = timezone.make_aware(datetime.combine(form.cleaned_data["start_date"], form.cleaned_data["start_time"]))
            series.teacher = current_user
            series.save()

            students = form.cleaned_data["students"]

            if series.repeat == Series.RepeatChoices.NEVER:
                delta = None

            elif series.repeat == Series.RepeatChoices.DAILY:
                delta = timedelta(days=1)

            elif series.repeat == Series.RepeatChoices.WEEKLY:
                delta = timedelta(days=7)

            # only RepeatChoice left is monthly
            else:
                delta = relativedelta(months=1)

            lesson_datetime = series.start_datetime
            # do-while loop implementation
            while True:
                lesson = Lesson(
                    series=series,
                    teacher=current_user,
                    datetime=lesson_datetime,
                    length=series.length,
                )
                lesson.save()
                lesson.students.set(students)

                for student in students:
                    student_status = StudentStatus(student=student, lesson=lesson)
                    student_status.save()

                lesson_datetime += delta
                if lesson_datetime.date() > form.cleaned_data["end_date"] or not delta:
                    break
                
            if (amount := form.cleaned_data["amount"]):
                for student in students:    
                    transaction_record = get_create_transaction_record(current_user, student)

                    transaction = Transaction(
                        sender=current_user,
                        receiver=student,
                        last_sent_by=current_user,
                        transaction_record=transaction_record,
                        amount=amount,
                        note="fee for " + form.cleaned_data["name"],
                        series=series,
                    )
                    transaction.save()

            return HttpResponseRedirect(reverse("lesson_planner:index"))

    else:
        form = CreateSeriesForm(current_user.id)

    context = {"form": form}

    return render(request, "lesson_planner/create_series.html", context)


@login_required
def request_series(request):
    current_user = request.user

    if request.method == "POST":
        form = RequestSeriesForm(current_user.id, data=request.POST)

        if form.is_valid():
            series = form.save()
            series.status = series.StatusChoices.REQUEST
            series.start_datetime = datetime.combine(form.cleaned_data["start_date"], form.cleaned_data["start_time"])
            series.save()

            return HttpResponseRedirect(reverse("lesson_planner:index"))

    else:
        form = RequestSeriesForm(current_user.id)

    context = {"form": form}

    return render(request, "lesson_planner/request_series.html", context=context)


@login_required
def edit_series(request, series_id):
    current_user = request.user
    series = Series.objects.get(id=series_id)

    if request.method == "POST":
        form = CreateSeriesForm(current_user.id, instance=series, data=request.POST)

        if form.is_valid():
            # TODO: edit relevant fields on all sub-lessons
            form.save()

            return HttpResponseRedirect(reverse("lesson_planner:index"))

    else:
        form = CreateSeriesForm(current_user.id, instance=series)

    context = {"form": form, "series_id": series_id}

    return render(request, "lesson_planner/edit_series.html", context)


@login_required
def edit_lesson(request, lesson_id):
    current_user = request.user
    lesson = Lesson.objects.get(id=lesson_id)

    if request.method == "POST":
        form = CreateLessonForm(instance=lesson, data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("lesson_planner:index"))

    else:
        form = CreateLessonForm(instance=lesson)

    context = {"form": form, "lesson_id": lesson_id}

    return render(request, "lesson_planner/edit_lesson.html", context)
