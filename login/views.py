from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def render_homepage(request):
    return render(request, 'index.html')

def render_login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print("User logged in successfully")
            return redirect('/')
        
        else:
            messages.info(request, "Invalid credentials.")
            return render(request, 'login.html')
        
    return render(request, 'login.html')

def render_signup_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken.")
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already registered.")
            return render(request, 'signup.html')

        if password != confirm_password:
            messages.info(request, "Passwords do not match.")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        print("User created successfully")
        return redirect('login')
    
    return render(request, 'signup.html')

def render_reset_password_page(request):


    context = {
        "emailFoundStatus": False,
        "passwordMatchStatus": False,
        "displaySignupLink": False,
        "emailMessage": "",
        "passwordMessage": ""
    }

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'lookup':
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
                context["email"] = email
                print(f'Email : {email}')
                context["emailFoundStatus"] = True
                context["emailMessage"] = f"Your Username is : {user.username}"
            except User.DoesNotExist:
                context["emailFoundStatus"] = False
                context["displaySignupLink"] = True
                context["emailMessage"] = "Email not found"

        elif action == 'reset':
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            print(f'Password: {password}, Confirm Password: {confirm_password}')
            try:
                user = User.objects.get(email=email)
                if password and password == confirm_password:
                    user.set_password(password)
                    user.save()
                    context["emailFoundStatus"] = True
                    context["passwordMatchStatus"] = True
                    context["passwordMessage"] = "Password reset successfully"
                else:
                    context["emailFoundStatus"] = True
                    context["passwordMatchStatus"] = False
                    context["passwordMessage"] = "Passwords do not match"
            except User.DoesNotExist:
                context["emailFoundStatus"] = False
                context["displaySignupLink"] = True
                context["emailMessage"] = "Email not found"

    return render(request, 'resetPassword.html', {'context': context})