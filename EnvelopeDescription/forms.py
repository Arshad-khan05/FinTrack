from django import forms
from .models import EnvelopeDescription
from Envelopes.models import Envelope_Home

class EnvelopeDescriptionForm(forms.ModelForm):
    class Meta:
        model = EnvelopeDescription
        fields = ['EnvelopeName', 'Description', 'Money_Spent']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['EnvelopeName'].queryset = (
                Envelope_Home.objects.filter(username=user)
            )
