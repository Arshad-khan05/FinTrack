from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from Envelopes.models import Envelope_Home
from EnvelopeDescription.models import EnvelopeDescription
from django.db.models import Sum

# Create your views here.
def render_homepage(request):
    if request.user.is_authenticated:
        # Get all envelopes for the user
        envelopes = Envelope_Home.objects.filter(username=request.user)
        
        # Calculate totals
        total_allocated = envelopes.aggregate(Sum('Money_Allocated'))['Money_Allocated__sum'] or 0
        total_spent = envelopes.aggregate(Sum('Money_Spent'))['Money_Spent__sum'] or 0
        total_remaining = total_allocated - total_spent
        total_envelopes = envelopes.count()
        
        context = {
            'total_allocated': total_allocated,
            'total_spent': total_spent,
            'total_remaining': total_remaining,
            'total_envelopes': total_envelopes,
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



def delete_user_account(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('homepage')