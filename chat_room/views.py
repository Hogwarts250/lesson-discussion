from django.shortcuts import render

from transactions.models import TransactionRecord, Transaction
from users.models import User

# Create your views here.
def index(request):
    transaction_records = TransactionRecord.objects.filter(users__id=request.user.id)
    users = User.objects.filter(transactionrecord__in=transaction_records).exclude(id=request.user.id)

    context = {"users": users}

    return render(request, "chat_room/index.html", context)

def room(request, user_id):
    user_transaction_records = TransactionRecord.objects.filter(users__id=request.user.id)
    users = User.objects.filter(transactionrecord__in=user_transaction_records).exclude(id=request.user.id)

    transaction_record = user_transaction_records.filter(users__id=user_id)
    transactions = Transaction.objects.filter(transaction_record=transaction_record[0])

    context = {"users": users, "transactions": transactions}

    return render(request, "chat_room/room.html", context)
