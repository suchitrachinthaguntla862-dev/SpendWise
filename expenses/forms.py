from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "date", "note"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Lunch with friends"}),
            "amount": forms.NumberInput(attrs={"placeholder": "0.00", "min": "0.01", "step": "0.01"}),
            "date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.TextInput(attrs={"placeholder": "Optional note"}),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount
