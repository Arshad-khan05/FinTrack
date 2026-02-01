from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EnvelopeDescriptionForm
from Envelopes.models import Envelope_Home
from .models import EnvelopeDescription
# Create your views here.
@login_required(login_url='login')
def addEnvelopeDescription(request):
    if request.method == 'POST':
        form = EnvelopeDescriptionForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                envelope_description = form.save(commit=False)

                envelope = Envelope_Home.objects.get(id=envelope_description.EnvelopeName.id, username=request.user)
                
                if envelope_description.Money_Spent <= 0:
                    messages.warning(request, "Money spent must be greater than 0.")
                    return redirect('homepage')

                # Calculate projected totals (allow negative remaining with confirmation)
                projected_spent = envelope.Money_Spent + envelope_description.Money_Spent
                projected_remaining = envelope.Money_Allocated - projected_spent
                if projected_remaining < 0 and request.POST.get('confirm_overflow') != '1':
                    return render(request, 'FormEnvelopeDescription.html', {
                        'form': form,
                        'show_overflow_confirm': True,
                        'projected_remaining': projected_remaining,
                        'envelope': envelope
                    })

                envelope_description.username = request.user
                envelope_description.Money_Remaining = projected_remaining
                envelope_description.save()

                envelope.Money_Spent = projected_spent
                envelope.Money_Remaining = projected_remaining
                envelope.save()
                messages.success(request, "Expense recorded successfully.")
                return redirect('display_envelope_descriptions')
            except Envelope_Home.DoesNotExist:
                messages.error(request, "Selected envelope not found.")
                return redirect('homepage')
            except Exception as e:
                messages.error(request, "An error occurred while saving the expense.")
                return redirect('homepage')
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
                    'id': envSpendDescriptions.id,
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
                    

@login_required(login_url='login')
def displayEnvelopeDescriptions(request):

    descriptions = EnvelopeDescription.objects.filter(username=request.user)
    envelopes = Envelope_Home.objects.filter(username=request.user)
    
    descriptions = getfiltered_envelope_descriptions(descriptions, envelopes)
    return render(request, 'DisplayEnvelopeDescriptions.html', {'Descriptions': descriptions})


@login_required(login_url='login')
def deleteEnvelopeDescription(request, id):
    if request.method != 'POST':
        return redirect('display_envelope_descriptions')

    envelope_desc = get_object_or_404(EnvelopeDescription, id=id, username=request.user)

    # Reverse the amounts on the related envelope
    try:
        envelope = Envelope_Home.objects.get(id=envelope_desc.EnvelopeName.id, username=request.user)
    except Envelope_Home.DoesNotExist:
        envelope = None

    if envelope:
        # Reverse the spend and re-derive remaining from allocated to keep consistency.
        envelope.Money_Spent = max(0, envelope.Money_Spent - envelope_desc.Money_Spent)
        envelope.Money_Remaining = envelope.Money_Allocated - envelope.Money_Spent
        envelope.save()

    envelope_desc.delete()
    return redirect('display_envelope_descriptions')


@login_required(login_url='login')
def updateEnvelopeDescription(request, id):
    envelope_desc = get_object_or_404(EnvelopeDescription, id=id, username=request.user)
    old_envelope = envelope_desc.EnvelopeName
    old_spent = envelope_desc.Money_Spent

    if request.method == 'POST':
        # Disabled fields aren't submitted by the browser. Copy POST data
        # and inject the existing EnvelopeName so form validation passes.
        post = request.POST.copy()
        post['EnvelopeName'] = str(envelope_desc.EnvelopeName.id)

        form = EnvelopeDescriptionForm(post, instance=envelope_desc, user=request.user)
        if form.is_valid():
            updated = form.save(commit=False)

            # Force the envelope to remain unchanged during updates
            updated.EnvelopeName = envelope_desc.EnvelopeName

            new_spent = updated.Money_Spent
            if new_spent <= 0:
                messages.warning(request, "Money spent must be greater than 0.")
                return redirect('display_envelope_descriptions')
            # Adjust envelope totals by the delta between new and old spent
            delta = new_spent - old_spent
            try:
                env = Envelope_Home.objects.get(id=envelope_desc.EnvelopeName.id, username=request.user)
            except Envelope_Home.DoesNotExist:
                env = None
            if env:
                projected_spent = max(0, env.Money_Spent + delta)
                projected_remaining = env.Money_Allocated - projected_spent
                if projected_remaining < 0 and request.POST.get('confirm_overflow') != '1':
                    if 'EnvelopeName' in form.fields:
                        form.fields['EnvelopeName'].disabled = True
                    return render(request, 'UpdateEnvelopeDescription.html', {
                        'form': form,
                        'desc': envelope_desc,
                        'show_overflow_confirm': True,
                        'projected_remaining': projected_remaining,
                        'envelope': env
                    })
                env.Money_Spent = projected_spent
                env.Money_Remaining = projected_remaining
                env.save()

            # Update the description's Money_Remaining to reflect the current envelope remaining
            if env:
                updated.Money_Remaining = env.Money_Remaining
            else:
                updated.Money_Remaining = 0

            updated.username = request.user
            updated.save()
            return redirect('display_envelope_descriptions')
    else:
        form = EnvelopeDescriptionForm(instance=envelope_desc, user=request.user)
        # Disable envelope selection so user cannot change it
        if 'EnvelopeName' in form.fields:
            form.fields['EnvelopeName'].disabled = True

    return render(request, 'UpdateEnvelopeDescription.html', {'form': form, 'desc': envelope_desc})