from math import ceil

from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.utils import timezone

from .forms import TransactionForm, EditTransactionForm
from .models import TransactionRecord, Transaction
from lesson_planner.models import Lesson
from users.models import User

# Create your views here.
def get_create_transaction_record(user, other):
    if (transaction_record := TransactionRecord.objects.filter(users__id=user.id).filter(users__id=other.id)):
        transaction_record = transaction_record[0]

    else:
        transaction_record = TransactionRecord()
        transaction_record.save()
        transaction_record.users.add(user)
        transaction_record.users.add(other)

    return transaction_record

def confirm_deny_model(request, model_instance, **kwargs):
    post_keys = "".join([k for k in request.POST.keys() if k != "csrfmiddlewaretoken"])
    if "confirm" in post_keys:
        model_instance.set_status_confirmed(**kwargs)

    elif "send" in post_keys:
        model_instance.set_status_sent(**kwargs)

    elif "deny" in post_keys:
        model_instance.set_status_denied(**kwargs)

    elif "receive" in post_keys:
        model_instance.set_status_received(**kwargs)

def index(request, transaction_id=None):
    current_user = request.user

    if request.method == "POST":
        transaction = Transaction.objects.get(id=transaction_id)
        confirm_deny_model(request, transaction, user=current_user)

        return HttpResponseRedirect(reverse("transactions:index"))

    if current_user.is_authenticated:
        pending_transactions = Transaction.objects.filter(
            Q(sender=current_user) | Q(receiver=current_user)
        ).exclude(
            Q(status=Transaction.STATUS.received) | Q(status=Transaction.STATUS.denied)
        ).distinct()

        num_lessons = 3 if ceil(len(pending_transactions) / 2) < 3 else ceil(len(pending_transactions) / 2)
        lessons = Lesson.objects.filter(
            Q(teacher=current_user) | Q(students=current_user)
        ).distinct().filter(
            status=Lesson.StatusChoices.CREATE
        ).exclude(datetime__lte=timezone .now()).order_by("datetime")[:num_lessons]

        context = {"lessons": lessons, "pending_transactions": pending_transactions }

    else:
        context = {}

    return render(request, "transactions/index.html", context)

@login_required
def create_transaction(request):
    current_user = request.user

    if request.method == "POST":
        form = TransactionForm(user_id=current_user.id, data=request.POST)

        if form.is_valid():
            receiver = form.cleaned_data["receiver"]

            amount = form.cleaned_data["amount"]

            transaction_record = get_create_transaction_record(
                current_user, receiver)

            transaction = Transaction(
                sender=current_user,
                receiver=receiver,
                last_sent_by=current_user,
                transaction_record=transaction_record,
                send_request=form.cleaned_data["send_request"],
                amount=amount,
                note=form.cleaned_data["note"],
            )
            transaction.save()

            if form.cleaned_data["send_request"] == transaction.SendRequestChoices.SEND:
                transaction.set_status_sent(user=current_user)

            return HttpResponseRedirect(reverse("transactions:index"))

    else:
        form = TransactionForm(user_id=current_user.id)

    context = {"form": form}

    return render(request, "transactions/create_transaction.html", context)

@login_required
def edit_transaction(request, transaction_id):
    current_user = request.user
    transaction = Transaction.objects.get(id=transaction_id)

    if request.method == "POST":
        form = EditTransactionForm(instance=transaction, data=request.POST)
        post_keys = "".join([k for k in request.POST.keys() if k != "csrfmiddlewaretoken"])
        other = transaction.get_other_user(current_user)

        if "transaction" in post_keys:
            transaction = Transaction.objects.get(id=transaction_id)
            confirm_deny_model(request, transaction, user=current_user)

        elif form.is_valid():
            form.save()
            transaction.last_sent_by = transaction.get_other_user(transaction.last_sent_by)
            transaction.save()

        return HttpResponseRedirect(reverse("chat_room:index", args=[other.id]))

    else:
        form = EditTransactionForm(instance=transaction)

    context = {"form": form, "transaction_id": transaction_id, "transaction": transaction}

    return render(request, "transactions/edit_transaction.html", context)
