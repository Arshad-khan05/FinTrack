from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Envelopes.models import Envelope_Home
from EnvelopeDescription.models import EnvelopeDescription
from django.db.models import Sum
from Income.models import Income_Table, Income_Description
from django.contrib.auth import update_session_auth_hash

# Create your views here.
@login_required(login_url='login')
def render_homepage(request):
    if request.user.is_authenticated:
        # Get all envelopes for the user
        envelopes = Envelope_Home.objects.filter(username=request.user)
        
        # Calculate totals
        total_allocated = envelopes.aggregate(Sum('Money_Allocated'))['Money_Allocated__sum'] or 0
        total_spent = envelopes.aggregate(Sum('Money_Spent'))['Money_Spent__sum'] or 0
        total_remaining = total_allocated - total_spent
        total_envelopes = envelopes.count()
        # Income totals
        total_income = Income_Description.objects.filter(username=request.user).aggregate(Sum('Amount'))['Amount__sum'] or 0
        total_income_sources = Income_Table.objects.filter(username=request.user).count()
        
        context = {
            'total_allocated': total_allocated,
            'total_spent': total_spent,
            'total_remaining': total_remaining,
            'total_envelopes': total_envelopes,
            'total_income': total_income,
            'total_income_sources': total_income_sources,
        }
        return render(request, 'index.html', context)
    return render(request, 'index.html')

def render_login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')
        
    return render(request, 'login.html')

def render_signup_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname', '').strip()
        last_name = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm-password', '')
        terms_accepted = request.POST.get('terms', False)

        # Validate required fields
        if not all([first_name, last_name, email, username, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('signup')

        # Validate terms acceptance
        if not terms_accepted:
            messages.error(request, "You must accept the terms and conditions to proceed.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect('signup')

        try:
            user = User.objects.create_user(
                username=username, 
                password=password, 
                email=email, 
                first_name=first_name, 
                last_name=last_name
            )
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, "An error occurred during registration. Please try again.")
            return redirect('signup')
    
    return render(request, 'signup.html')
def render_reset_password_page(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'lookup':
            email = request.POST.get('email', '').strip()
            
            if not email:
                messages.error(request, "Email is required.")
                return redirect('reset_password')
            
            try:
                user = User.objects.get(email=email)
                return render(request, 'resetPassword.html', {
                    'email': email,
                    'username': user.username,
                    'show_password_form': True
                })
            except User.DoesNotExist:
                messages.error(request, "Email not found.")
                return redirect('reset_password')

        elif action == 'reset':
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')
            
            if not email or not password or not confirm_password:
                messages.error(request, "All fields are required.")
                return redirect('reset_password')
            
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('reset_password')
            
            if len(password) < 6:
                messages.error(request, "Password must be at least 6 characters long.")
                return redirect('reset_password')
            
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                messages.success(request, "Password reset successfully! Please log in with your new password.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('reset_password')
            except Exception as e:
                messages.error(request, "An error occurred while resetting password.")
                return redirect('reset_password')
    
    return render(request, 'resetPassword.html', {})


def logout_view(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def delete_user_account(request):
    # Show a confirmation page on GET. Only delete on POST.
    if request.method == 'POST':
        user = request.user
        logout(request)
        try:
            user.delete()
            messages.success(request, "Account deleted successfully.")
        except Exception:
            messages.error(request, "An error occurred while deleting the account.")
        return redirect('homepage')

    return render(request, 'confirm_delete_account.html', {})


@login_required(login_url='login')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('firstname', '').strip()
        last_name = request.POST.get('lastname', '').strip()

        # Update name fields
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        # Handle password change if requested
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        current_password = request.POST.get('current_password', '')

        if new_password or confirm_password or current_password:
            # require current password
            if not current_password:
                messages.error(request, "Current password is required to change your password.")
                return redirect('edit_profile')

            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
                return redirect('edit_profile')

            if not new_password or not confirm_password:
                messages.error(request, "New password and confirmation are required.")
                return redirect('edit_profile')

            if new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return redirect('edit_profile')

            if len(new_password) < 6:
                messages.error(request, "Password must be at least 6 characters long.")
                return redirect('edit_profile')

            try:
                user.set_password(new_password)
                user.save()
                # keep user logged in after password change
                update_session_auth_hash(request, user)
                messages.success(request, "Profile updated and password changed successfully.")
                return redirect('/')
            except Exception:
                messages.error(request, "An error occurred while changing password.")
                return redirect('edit_profile')

        # Save name changes if any
        try:
            user.save()
            messages.success(request, "Profile updated successfully.")
        except Exception:
            messages.error(request, "An error occurred while updating profile.")

        return redirect('/')

    # GET: render form with current values
    return render(request, 'edit_profile.html', {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'username': user.username,
    })