from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import *
from .models import TransactionRecord, Transaction
from users.models import User

# Create your views here.
def index(request):
    user = request.user

    if request.method == "POST":
        form = TransactionForm(user_id=user.id, data=request.POST)

        if form.is_valid():
            seller = User.objects.get(id=user.id)
            buyer = form.cleaned_data["buyer"]
            amount = form.cleaned_data["amount"]

            if (transaction_record := TransactionRecord.objects.filter(users__id=user.id).filter(users__id=buyer.id)):
                transaction_record = transaction_record[0]

            else:
                transaction_record = TransactionRecord()
                transaction_record.save()
                transaction_record.users.add(buyer)
                transaction_record.users.add(seller)

            transaction = Transaction(
                buyer=buyer,
                seller=seller,
                last_sent_by=user,
                transaction_record=transaction_record,
                amount=amount,
            )
            transaction.save()

            form = TransactionForm(user_id=user.id)

    else:
        form = TransactionForm(user_id=user.id)

    context = {"form": form}

    return render(request, "transactions/index.html", context)


def edit_transaction(request, transaction_id):
    current_user = request.user
    transaction = Transaction.objects.get(id=transaction_id)

    if request.method == "POST":
        form = TransactionForm(user_id=current_user.id,
                               instance=transaction, data=request.POST)
        other = transaction.get_other_user(current_user)

        if form.is_valid():
            if "confirm_transaction" in request.POST:
                transaction.set_status_confirmed()

            elif "deny_transaction" in request.POST:
                transaction.set_status_denied()

            else:
                form.save()
                transaction.last_sent_by = transaction.get_other_user(
                    transaction.last_sent_by)
                transaction.save()

            return HttpResponseRedirect(reverse("chat_room:room", args=[other.id]))

    else:
        form = TransactionForm(current_user.id, instance=transaction)

    context = {"form": form, "transaction_id": transaction_id}

    return render(request, "transactions/edit_transaction.html", context)
