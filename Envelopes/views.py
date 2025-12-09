from urllib import request
from django.shortcuts import render
from .models import Envelope_Home
from django.contrib import messages

# Create your views here.

def display_index(request):
    if request.method == 'POST':
        print("POST request received in envelopes index view")
        username_id = request.user.id
        envelope_name = str(request.POST.get('envelope_name'))
        money_allocated = int(request.POST.get('money_allocated'))
        money_remaining = int(money_allocated)
        money_spent = int(money_allocated) - int(money_remaining)
        new_envelope = Envelope_Home(
            username_id=int(username_id),
            Envelope_Name=str(envelope_name),
            Money_Allocated=int(money_allocated),
            Money_Remaining=int(money_remaining),
            Money_Spent=int(money_spent)
        )
        new_envelope.save()
        print(f"{new_envelope} : New envelope created and saved successfully")
        messages.success(request, f"New envelope with name {envelope_name} and money allocated {money_allocated} created and saved successfully to user {request.user.username}")    
    return render(request, 'addenvelope.html')



def display_envelopes(request):
    envelopes = Envelope_Home.objects.filter(username=request.user)
    print(f"Envelopes for user {request.user.username}: {envelopes}")

    for envelope in envelopes:
        print(f"Envelope Name: {envelope.Envelope_Name}, Money Allocated: {envelope.Money_Allocated}, Money Remaining: {envelope.Money_Remaining}, Money Spent: {envelope.Money_Spent}, Created At: {envelope.Created_At}")

    return render(request, 'displayenvelope.html', {'envelopes': envelopes})





def update_envelope(request):
    return render(request, 'updateenvelope.html')