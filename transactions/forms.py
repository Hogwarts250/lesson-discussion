from django import forms
from django.conf import settings

from .models import Transaction
from users.models import User

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["receiver", "send_request", "amount", "note"]

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["receiver"].queryset = User.objects.exclude(id=user_id)
        
    receiver = forms.ModelChoiceField(
        queryset = None,
        empty_label = None
    )


class EditTransactionForm(forms.ModelForm):
    class Meta(TransactionForm.Meta):
        fields = ["amount"]
