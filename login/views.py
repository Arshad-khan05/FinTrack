from django.shortcuts import render

# Create your views here.
def render_homepage(request):
    return render(request, 'index.html')