from django.shortcuts import render

# Create your views here.
def render_homepage(request):
    return render(request, 'index.html')

def render_login_page(request):
    return render(request, 'login.html')

def render_signup_page(request):
    return render(request, 'signup.html')

def render_reset_password_page(request):
    return render(request, 'resetPassword.html')