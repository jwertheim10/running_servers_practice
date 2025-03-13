from django import forms
from .models import Accounts

class AccountsForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password']