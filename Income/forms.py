from django import forms
from .models import Income_Description, Income_Table


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income_Table
        fields = ['IncomeName']


class IncomeDescriptionForm(forms.ModelForm):
    class Meta:
        model = Income_Description
        fields = ['IncomeName', 'Description', 'Amount']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['IncomeName'].queryset = Income_Table.objects.filter(username=user)
