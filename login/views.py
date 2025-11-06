from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages as message
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
            return redirect('/')
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
            message.info(request, "Username already taken.")
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            message.info(request, "Email already registered.")
            return render(request, 'signup.html')

        if password != confirm_password:
            message.info(request, "Passwords do not match.")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        return redirect('login')
    
    return render(request, 'signup.html')

def render_reset_password_page(request):
    return render(request, 'resetPassword.html')