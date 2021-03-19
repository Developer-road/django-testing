from django import forms


class ExpenseForm(forms.Form):
    title = forms.CharField(max_length=100)
    amount = forms.IntegerField()
    category = forms.CharField()
