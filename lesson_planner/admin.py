from django.contrib import admin

from .models import TransactionRecord, Transaction, Lesson

# Register your models here.
admin.site.register(TransactionRecord)
admin.site.register(Transaction)
admin.site.register(Lesson)