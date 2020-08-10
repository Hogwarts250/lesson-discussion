from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import TransactionRecord, Transaction
from users.models import User

# Create your views here.
@login_required
def index(request):
    user = request.user

    if request.method == "POST":
        form = TransactionForm(data=request.POST)

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
                buyer = buyer, 
                seller = seller, 
                amount = amount, 
                transaction_record = transaction_record
            )
            transaction.save()

    form = TransactionForm()

    context = {"form": form}

    return render(request, "lesson_planner/index.html", context)
