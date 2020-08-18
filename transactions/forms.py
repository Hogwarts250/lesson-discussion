from django import forms
from django.conf import settings

from .models import Transaction
from users.models import User

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["buyer", "amount", "note"]

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["buyer"].queryset = User.objects.exclude(id=user_id)
        
    buyer = forms.ModelChoiceField(
        queryset = None,
        empty_label = None
    )
