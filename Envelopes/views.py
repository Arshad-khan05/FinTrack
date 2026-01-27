from urllib import request
from django.shortcuts import render, redirect
from .models import Envelope_Home
from django.contrib import messages
from .forms import EnvelopeForm
# Create your views here.



def display_addenvelope(request):
    if request.method == 'POST':
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
        messages.success(request, f"New envelope with name {envelope_name} and money allocated {money_allocated} created and saved successfully to user {request.user.username}")    
    return render(request, 'addenvelope.html')



def display_envelopes(request):
    envelopes = Envelope_Home.objects.filter(username=request.user)
    return render(request, 'displayenvelope.html', {'envelopes': envelopes})




def display_update_envelope(request):
    envelopes = Envelope_Home.objects.filter(username=request.user)
    return render(request, 'updateenvelope.html', {'envelopes': envelopes})



def update_envelope(request, envelope_id):
    
    if request.method == 'POST':
        envelope_name = str(request.POST.get('name'))
        money_allocated = int(request.POST.get('budget'))
        money_spent = int(request.POST.get('spend'))
        money_remaining = money_allocated - money_spent

        envelope = Envelope_Home.objects.get(id=envelope_id, username=request.user)
        envelope.Envelope_Name = envelope_name
        envelope.Money_Allocated = money_allocated
        envelope.Money_Spent = money_spent
        envelope.Money_Remaining = money_allocated - money_spent
        envelope.save()
        return redirect('updateenvelope')
    


    envelope = Envelope_Home.objects.get(id=envelope_id, username=request.user)        
    return render(request, 'updateenvelopeform.html', {'envelope': envelope})



def delete_envelope(request, envelope_id):
    envelope = Envelope_Home.objects.get(id=envelope_id, username=request.user)
    envelope.delete()
    return redirect('updateenvelope')