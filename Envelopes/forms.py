from django import forms
from .models import Envelope_Home

class EnvelopeForm(forms.ModelForm):
    class Meta:
        model = Envelope_Home
        fields = ['Envelope_Name', 'Money_Allocated','Money_Remaining']
