from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Envelope_Home
from django.contrib import messages
from .forms import EnvelopeForm
# Create your views here.



@login_required(login_url='login')
def display_addenvelope(request):
    if request.method == 'POST':
        try:
            username_id = request.user.id
            envelope_name = request.POST.get('envelope_name', '').strip()
            money_allocated = request.POST.get('money_allocated', '').strip()
            
            if not envelope_name:
                messages.error(request, "Envelope name is required.")
                return redirect('addenvelope')
            
            if not money_allocated:
                messages.error(request, "Money allocated is required.")
                return redirect('addenvelope')
            
            try:
                money_allocated = int(money_allocated)
                if money_allocated <= 0:
                    messages.error(request, "Money allocated must be greater than 0.")
                    return redirect('addenvelope')
            except ValueError:
                messages.error(request, "Money allocated must be a valid number.")
                return redirect('addenvelope')
            
            money_spent = 0
            money_remaining = money_allocated - money_spent
            if money_remaining < 0:
                messages.warning(request, "Remaining amount cannot be negative.")
                return redirect('addenvelope')
            
            new_envelope = Envelope_Home(
                username_id=int(username_id),
                Envelope_Name=envelope_name,
                Money_Allocated=money_allocated,
                Money_Remaining=money_remaining,
                Money_Spent=money_spent
            )
            new_envelope.save()
            messages.success(request, f"New envelope '{envelope_name}' with budget {money_allocated} created successfully.")
            return redirect('addenvelope')
        except Exception as e:
            messages.error(request, "An error occurred while creating the envelope.")
            return redirect('addenvelope')
    
    return render(request, 'addenvelope.html')



@login_required(login_url='login')
def display_envelopes(request):
    envelopes = Envelope_Home.objects.filter(username=request.user)
    return render(request, 'displayenvelope.html', {'envelopes': envelopes})




@login_required(login_url='login')
def display_update_envelope(request):
    envelopes = Envelope_Home.objects.filter(username=request.user)
    return render(request, 'updateenvelope.html', {'envelopes': envelopes})



@login_required(login_url='login')
def update_envelope(request, envelope_id):
    try:
        envelope = Envelope_Home.objects.get(id=envelope_id, username=request.user)
    except Envelope_Home.DoesNotExist:
        messages.error(request, "Envelope not found.")
        return redirect('updateenvelope')
    
    if request.method == 'POST':
        try:
            envelope_name = request.POST.get('name', '').strip()
            money_allocated = request.POST.get('budget', '').strip()
            money_spent = request.POST.get('spend', '').strip()
            
            if not envelope_name:
                messages.error(request, "Envelope name is required.")
                return redirect('updateenvelope')
            
            if not money_allocated or not money_spent:
                messages.error(request, "All fields are required.")
                return redirect('updateenvelope')
            
            try:
                money_allocated = int(money_allocated)
                money_spent = int(money_spent)
                
                if money_allocated < 0 or money_spent < 0:
                    messages.error(request, "Amounts cannot be negative.")
                    return redirect('updateenvelope')
            except ValueError:
                messages.error(request, "Money values must be valid numbers.")
                return redirect('updateenvelope')
            
            money_remaining = money_allocated - money_spent
            if money_remaining < 0:
                messages.warning(request, "This update makes the remaining balance negative.")
            
            envelope.Envelope_Name = envelope_name
            envelope.Money_Allocated = money_allocated
            envelope.Money_Spent = money_spent
            envelope.Money_Remaining = money_remaining
            envelope.save()
            messages.success(request, "Envelope updated successfully.")
            return redirect('updateenvelope')
        except Exception as e:
            messages.error(request, "An error occurred while updating the envelope.")
            return redirect('updateenvelope')
    
    return render(request, 'updateenvelopeform.html', {'envelope': envelope})



@login_required(login_url='login')
def delete_envelope(request, envelope_id):
    envelope = Envelope_Home.objects.filter(id=envelope_id, username=request.user).first()
    if not envelope:
        messages.error(request, "Envelope not found.")
        return redirect('updateenvelope')
    envelope.delete()
    return redirect('updateenvelope')