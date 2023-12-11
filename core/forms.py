from django import forms

from . models import Transaction, Category


class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = "__all__"
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Give a description....'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


