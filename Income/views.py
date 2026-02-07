from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Income_Table, Income_Description
from .forms import IncomeForm, IncomeDescriptionForm


@login_required(login_url='login')
def add_income(request):
    if request.method == 'POST':
        name = request.POST.get('income_name', '').strip()
        if not name:
            messages.error(request, "Income name is required.")
            return redirect('add_income')
        if Income_Table.objects.filter(username=request.user, IncomeName__iexact=name).exists():
            messages.error(request, "You already have an income source with that name.")
            return redirect('add_income')
        Income_Table.objects.create(username=request.user, IncomeName=name)
        messages.success(request, "Income source created.")
        return redirect('add_income')
    return render(request, 'addincome.html')


@login_required(login_url='login')
def display_incomes(request):
    incomes = Income_Table.objects.filter(username=request.user)
    return render(request, 'displayincome.html', {'incomes': incomes})


@login_required(login_url='login')
def update_incomes(request):
    incomes = Income_Table.objects.filter(username=request.user)
    return render(request, 'updateincome.html', {'incomes': incomes})


@login_required(login_url='login')
def edit_income(request, income_id):
    inc = get_object_or_404(Income_Table, id=income_id, username=request.user)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, "Income name is required.")
            return redirect('update_income')
        inc.IncomeName = name
        inc.save()
        messages.success(request, "Income source updated.")
        return redirect('update_income')
    return render(request, 'updateincomeform.html', {'income': inc})


@login_required(login_url='login')
def delete_income(request, income_id):
    inc = Income_Table.objects.filter(id=income_id, username=request.user).first()
    if inc:
        inc.delete()
    return redirect('update_income')


@login_required(login_url='login')
def add_income_description(request):
    if request.method == 'POST':
        form = IncomeDescriptionForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                desc = form.save(commit=False)
                desc.username = request.user
                desc.save()
                messages.success(request, "Income recorded successfully.")
                return redirect('display_income_descriptions')
            except Exception:
                messages.error(request, "Error saving income description.")
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = IncomeDescriptionForm(user=request.user)
    return render(request, 'FormIncomeDescription.html', {'form': form})


def getfiltered_income_descriptions(descriptions, incomes):
    result = {}
    for income in incomes:
        name = income.IncomeName
        items = []
        for d in descriptions:
            if d.IncomeName.id == income.id:
                items.append({'id': d.id, 'Description': d.Description, 'Amount': d.Amount, 'Date': d.created_at})
        # include current total for this income source so templates can show updated totals
        if name not in result:
            result[name] = {'Income': name, 'Descriptions': items, 'Total': income.Total_Amount}
    return result


@login_required(login_url='login')
def display_income_descriptions(request):
    from django.utils import timezone
    now = timezone.now()
    descriptions = Income_Description.objects.filter(username=request.user, created_at__month=now.month, created_at__year=now.year)
    incomes = Income_Table.objects.filter(username=request.user)
    descriptions = getfiltered_income_descriptions(descriptions, incomes)
    return render(request, 'DisplayIncomeDescriptions.html', {'Descriptions': descriptions})


@login_required(login_url='login')
def delete_income_description(request, id):
    if request.method != 'POST':
        return redirect('display_income_descriptions')
    desc = get_object_or_404(Income_Description, id=id, username=request.user)
    try:
        desc.delete()
    except Exception:
        pass
    return redirect('display_income_descriptions')


@login_required(login_url='login')
def update_income_description(request, id):
    desc = get_object_or_404(Income_Description, id=id, username=request.user)
    old_amount = desc.Amount
    if request.method == 'POST':
        post = request.POST.copy()
        post['IncomeName'] = str(desc.IncomeName.id)
        form = IncomeDescriptionForm(post, instance=desc, user=request.user)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.IncomeName = desc.IncomeName
            new_amount = updated.Amount
            if new_amount <= 0:
                messages.warning(request, "Amount must be greater than 0.")
                return render(request, 'UpdateIncomeDescription.html', {'form': form, 'desc': desc})
            # adjust parent total via save()
            updated.username = request.user
            updated.save()
            messages.success(request, "Income description updated.")
            return redirect('display_income_descriptions')
    else:
        form = IncomeDescriptionForm(instance=desc, user=request.user)
        if 'IncomeName' in form.fields:
            form.fields['IncomeName'].disabled = True
    return render(request, 'UpdateIncomeDescription.html', {'form': form, 'desc': desc})
