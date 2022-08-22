import re
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from .forms import *
from .models import *
from pprint import pprint

# Create your views here.
def home(request):
    return render(request, 'home/dashboard.html')

def login(request):
    if request.method == 'POST':
        nid = request.POST.get('nid')
        password = request.POST.get('password')
        
        print(nid, password)
        
        
        user = authenticate(nid=nid, password=password)
        print("User:",user)
        if user is not None:
            login_user(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'home/login.html')

def dashboard(request):
    if request.user.is_authenticated:
        print('Authenticated User:', request.user.nid)
        return render(request, 'home/dashboard.html')
    else:
        return HttpResponse('Unauthorized')

def createslot(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'home/createslot.html')

def signup(request):
    if request.method == 'POST':
        pprint(request.POST)
        user_name = request.POST.get('name')
        user_nid = request.POST.get('nid')
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        user_contact = request.POST.get('contact')
        user_type = request.POST.get('is_owner')

        user = Users.objects.create(nid=user_nid, password=user_password, name=user_name, email=user_email, contact=user_contact, is_owner=user_type)
        user.save()
        messages.success(request, 'User created successfully')
        user.set_password(user_password)
        user.save()
        auth_user = authenticate(nid=user_nid, password=user_password)
        print("auth_user:",auth_user)
        return redirect('dashboard')
    else:
        return render(request, 'home/signup.html')



def logout(request):
    print('Logout User:', request.user.nid)
    logout_user(request)
    return redirect('login')