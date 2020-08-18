from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Lesson, StudentStatus
from .forms import LessonForm, RequestLessonForm
from transactions.models import Transaction
from transactions.views import get_create_transaction_record, confirm_deny_model
from users.models import User

# Create your views here.
def index(request, model_id=None):
    lessons = Lesson.objects.all()

    if request.method == "POST":
        post_keys = "".join([k for k in request.POST.keys() if k != "csrfmiddlewaretoken"])
        print(post_keys)
        if "lesson" in post_keys:
            student_status = StudentStatus.objects.get(id=model_id)
            confirm_deny_model(request, student_status, "lesson_planner:index")

        elif "transaction" in post_keys:
            transaction = Transaction.objects.get(id=model_id)
            confirm_deny_model(request, transaction, "lesson_planner:index")

    context = {"lessons": lessons}

    return render(request, "lesson_planner/index.html", context)

# force current user to be the teacher? (or they just have to be a participant)
def create_lesson(request):
    current_user = request.user

    if request.method == "POST":
        form = LessonForm(user_id=current_user.id, data=request.POST)

        if form.is_valid():
            lesson = form.save()
            lesson.teacher = current_user
            lesson.save()

            for student in form.cleaned_data["students"]:
                if (amount := form.cleaned_data["amount"]):
                    transaction_record = get_create_transaction_record(current_user, student)

                    transaction = Transaction(
                        buyer=student,
                        seller=current_user,
                        last_sent_by=current_user,
                        transaction_record=transaction_record,
                        amount=amount,
                        note="fee for " + form.cleaned_data["name"],
                        lesson=lesson,
                    )
                    transaction.save()

                student_status = StudentStatus(student=student, lesson=lesson)
                student_status.save()
            
            return HttpResponseRedirect(reverse("lesson_planner:index"))

    else:
        form = LessonForm(user_id=current_user.id)

    context = {"form": form}

    return render(request, "lesson_planner/create_lesson.html", context)

def edit_lesson(request, lesson_id):
    current_user = request.user
    lesson = Lesson.objects.get(id=lesson_id)

    if request.method == "POST":
        form = LessonForm(instance=lesson, data=request.POST)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse("lesson_planner:index"))

    else:
        form = LessonForm(instance=lesson)

    context = {"form": form, "lesson_id": lesson_id}

    return render(request, "lesson_planner/edit_lesson.html", context)
