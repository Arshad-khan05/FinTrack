from django.shortcuts import render
from .forms import EnvelopeDescriptionForm
from Envelopes.models import Envelope_Home
from .models import EnvelopeDescription
# Create your views here.
def addEnvelopeDescription(request):
    if request.method == 'POST':
        form = EnvelopeDescriptionForm(request.POST, user=request.user)
        if form.is_valid():
            envelope_description = form.save(commit=False)

            CurrentMoneyRemaininginEnvelope = Envelope_Home.objects.get(id=envelope_description.EnvelopeName.id, username=request.user).Money_Remaining

            envelope_description.username = request.user
            envelope_description.Money_Remaining = CurrentMoneyRemaininginEnvelope - envelope_description.Money_Spent
            envelope_description.save()

            CurrentMoneyRemaininginEnvelope -= envelope_description.Money_Spent
            envelope = Envelope_Home.objects.get(id=envelope_description.EnvelopeName.id, username=request.user)
            envelope.Money_Remaining = CurrentMoneyRemaininginEnvelope
            envelope.Money_Spent += envelope_description.Money_Spent
            envelope.save()
    else:
        form = EnvelopeDescriptionForm(user=request.user)
    return render(request, 'FormEnvelopeDescription.html', {'form': form})

def getfiltered_envelope_descriptions(descriptions, envelopes):
    result = {}

    for envelope in envelopes:
        envName = envelope.Envelope_Name
        spendDescription = []
        for envSpendDescriptions in descriptions:
            if envSpendDescriptions.EnvelopeName.id == envelope.id:
                Description = {
                    'Description': envSpendDescriptions.Description,
                    'Money_Spent': envSpendDescriptions.Money_Spent,
                    'Money_Remaining': envSpendDescriptions.Money_Remaining,
                    'Date': envSpendDescriptions.created_at }
                
                spendDescription.append(Description)

        if envName not in result:
            result[envName] = {
                "Envelope" : envName,
                "Description":spendDescription
                }

    return result
                    

def displayEnvelopeDescriptions(request):

    descriptions = EnvelopeDescription.objects.filter(username=request.user)
    envelopes = Envelope_Home.objects.filter(username=request.user)
    
    descriptions = getfiltered_envelope_descriptions(descriptions, envelopes)
    return render(request, 'DisplayEnvelopeDescriptions.html', {'Descriptions': descriptions})