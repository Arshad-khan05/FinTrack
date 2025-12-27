from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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

        
        context = {
            "accountCreated": False,
            "createdmessage": "Account created successfully"
        }

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        context["accountCreated"] = True
        print("User created successfully")
        return render(request, 'signup.html', {'context':context})
    
    return render(request, 'signup.html', {'context':{}})
def render_reset_password_page(request):
    
    context = {
        "email": "",
        "emailMessage": "",
        "emailFoundStatus": False,
        "displayEmailFoundMessage": False,
        "displayEmailnotFoundMessage": False,
        "passwordMatchStatus": False,
        "passwordMessage": "",
        "displayPasswordMatchMessage": False,
        "displayPasswordNotMatchMessage": False
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'lookup':
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
                context["email"] = email
                context["emailMessage"] = f"Your username is: {user.username}"
                context["emailFoundStatus"] = True
                context["displayEmailFoundMessage"] = True
            except User.DoesNotExist:
                print("Email not found")
                context["emailMessage"] = "Email not found"
                context["emailFoundStatus"] = False
                context["displayEmailnotFoundMessage"] = True

        if action == 'reset':
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            print(f'Email: {email}')
            print(f'Password: {password}, Confirm Password: {confirm_password}')
            
            user = User.objects.get(email=email)
            if password is not None and password == confirm_password:
                user.set_password(password)
                user.save()
                print("Password reset successfully")
                context["passwordMatchStatus"] = True
                context["passwordMessage"] = "Password reset successfully"
                context["displayPasswordMatchMessage"] = True
            else:
                print("Passwords do not match")
                context["passwordMatchStatus"] = False
                context["passwordMessage"] = "Passwords do not match"
                context["displayPasswordNotMatchMessage"] = True
    return render(request, 'resetPassword.html', {'context': context})


def logout_view(request):
    logout(request)
    return redirect('/')



def delete_user_account(request):
    user = request.user
    logout(request)

        
    user.delete()
    print("User account deleted successfully")
    return redirect('/')