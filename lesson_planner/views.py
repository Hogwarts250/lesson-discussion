from datetime import datetime, timedelta
from dateutil import relativedelta

from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import Series, Lesson, StudentStatus
from .forms import SeriesForm, CreateLessonForm, RequestLessonForm
from transactions.models import Transaction
from transactions.views import get_create_transaction_record, confirm_deny_model
from users.models import User

# Create your views here.


@login_required
def index(request, model_id=None):
    current_user = request.user
    lessons = Lesson.objects.filter(
        Q(teacher=current_user) | Q(students=current_user)
    ).distinct()
    requested_lessons = lessons.filter(status=Lesson.StatusChoices.REQUEST)
    created_lessons = lessons.filter(status=Lesson.StatusChoices.CREATE)

    if request.method == "POST":
        post_keys = "".join([k for k in request.POST.keys()
                             if k != "csrfmiddlewaretoken"])
        if "lesson" in post_keys:
            lesson = lessons.get(id=model_id)
            confirm_deny_model(request, lesson)

            # if lesson.amount:
            #     for student in lesson.students.all():
            #         transaction_record = get_create_transaction_record(current_user, student)

            #         transaction = Transaction(
            #             sender=current_user,
            #             receiver=student,
            #             last_sent_by=current_user,
            #             transaction_record=transaction_record,
            #             amount=lesson.amount,
            #             note="fee for " + lesson.name,
            #             series=series,
            #         )
            #         transaction.save()

            #         student_status = StudentStatus(student=student, lesson=lesson)
            #         student_status.save()

        elif "student" in post_keys:
            student_status = StudentStatus.objects.get(id=model_id)
            confirm_deny_model(request, student_status)

        elif "transaction" in post_keys:
            transaction = Transaction.objects.get(id=model_id)
            confirm_deny_model(request, transaction, user=current_user)

        return HttpResponseRedirect(reverse("lesson_planner:index"))

    context = {"requested_lessons": requested_lessons,
               "created_lessons": created_lessons}

    return render(request, "lesson_planner/index.html", context)


@login_required
def create_lesson(request):
    current_user = request.user

    if request.method == "POST":
        lesson_form = CreateLessonForm(
            user_id=current_user.id, data=request.POST, prefix="lesson")
        series_form = SeriesForm(data=request.POST, prefix="series")

        if lesson_form.is_valid() and series_form.is_valid():
            series = series_form.save()

            if series_form.cleaned_data["repeat"] == Series.RepeatChoices.NEVER:
                lesson = lesson_form.save()
                lesson.series = series
                lesson.teacher = current_user
                lesson.datetime = series_form.cleaned_data["start_datetime"]
                lesson.save()

            else:
                if series_form.cleaned_data["repeat"] == Series.RepeatChoices.DAILY:
                    delta = timedelta(days=1)

                elif series_form.cleaned_data["repeat"] == Series.RepeatChoices.WEEKLY:
                    delta = timedelta(days=7)

                elif series_form.cleaned_data["repeat"] == Series.RepeatChoices.MONTHLY:
                    delta = relativedelta(months=1)
                else:
                    delta = timedelta(days=1)

                lesson_datetime = series_form.cleaned_data["start_datetime"]
                while lesson_datetime.date() <= series_form.cleaned_data["end_date"]:
                    lesson = Lesson(
                        series=series,
                        name=lesson_form.cleaned_data["name"],
                        teacher=current_user,
                        datetime=lesson_datetime,
                    )
                    lesson.save()
                    lesson.students.set(lesson_form.cleaned_data["students"])

                    for student in lesson_form.cleaned_data["students"]:
                        if (amount := series_form.cleaned_data["amount"]):
                                transaction_record = get_create_transaction_record(current_user, student)

                                transaction = Transaction(
                                    sender=current_user,
                                    receiver=student,
                                    last_sent_by=current_user,
                                    transaction_record=transaction_record,
                                    amount=amount,
                                    note="fee for " + lesson_form.cleaned_data["name"],
                                    series=series,
                                )
                                transaction.save()

                        student_status = StudentStatus(student=student, lesson=lesson)
                        student_status.save()

                    lesson_datetime += delta

            return HttpResponseRedirect(reverse("lesson_planner:index"))

    else:
        lesson_form = CreateLessonForm(
            user_id=current_user.id, prefix="lesson")
        series_form = SeriesForm(prefix="series")

    context = {"lesson_form": lesson_form, "series_form": series_form}

    return render(request, "lesson_planner/create_lesson.html", context)


@login_required
def request_lesson(request):
    current_user = request.user

    if request.method == "POST":
        request_form = RequestLessonForm(
            user_id=current_user.id, data=request.POST, prefix="request")
        series_form = SeriesForm(data=request.POST, prefix="series")

        if request_form.is_valid() and request_form.is_valid():
            lesson = request_form.save()
            lesson.status = lesson.StatusChoices.REQUEST
            lesson.save()

            return HttpResponseRedirect(reverse("lesson_planner:index"))

    else:
        request_form = RequestLessonForm(
            user_id=current_user.id, prefix="request")
        series_form = SeriesForm(prefix="series")

    context = {"request_form": request_form, "series_form": series_form}

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
