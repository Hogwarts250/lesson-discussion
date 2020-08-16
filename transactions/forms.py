from django import forms
from django.conf import settings

from .models import Transaction
from users.models import User

class TransactionForm(forms.ModelForm):
    buyer = forms.ModelChoiceField(
        queryset = None,
        empty_label = None
    )

    class Meta:
        model = Transaction
        fields = ["buyer", "amount"]

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["buyer"].queryset = User.objects.exclude(id=user_id)
        