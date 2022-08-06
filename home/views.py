from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'base-sidebar.html')

def login(request):
    return render(request, 'home/login.html')

def dashboard(request):
    return render(request, 'home/dashboard.html')