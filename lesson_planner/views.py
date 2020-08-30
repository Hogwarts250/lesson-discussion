from datetime import datetime, timedelta
from dateutil import relativedelta

from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import Series, Lesson, StudentStatus
from .forms import CreateSeriesForm, RequestSeriesForm # CreateLessonForm, RequestLessonForm
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

        elif "student" in post_keys:
            student_status = StudentStatus.objects.get(id=model_id)
            confirm_deny_model(request, student_status)

        elif "transaction" in post_keys:
            transaction = Transaction.objects.get(id=model_id)
            confirm_deny_model(request, transaction, user=current_user)

        return HttpResponseRedirect(reverse("lesson_planner:index"))

    context = {"requested_series": requested_series, "created_series": created_series}

    return render(request, "lesson_planner/index.html", context)


@login_required
def create_lesson(request):
    current_user = request.user

    if request.method == "POST":
        form = CreateSeriesForm(current_user.id, data=request.POST)

        if form.is_valid():
            series = form.save()
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

            lesson_datetime = form.cleaned_data["start_datetime"]
            # do-while loop implementation
            while condition:
                lesson = Lesson(
                    series=series,
                    teacher=current_user,
                    datetime=lesson_datetime,
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

    return render(request, "lesson_planner/create_lesson.html", context)


@login_required
def request_lesson(request):
    current_user = request.user

    if request.method == "POST":
        form = RequestSeriesForm(current_user.id, data=request.POST)

        if form.is_valid():
            series = form.save()
            series.status = series.StatusChoices.REQUEST
            series.save()

            return HttpResponseRedirect(reverse("lesson_planner:index"))

    else:
        form = RequestSeriesForm(current_user.id)

    context = {"form": form}

    return render(request, "lesson_planner/request_lesson.html", context=context)


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
