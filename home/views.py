import re
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from .forms import SpotForm, UserForm
from .models import *
from pprint import pprint
from django.core.mail import send_mail  
from PrimePark import settings  
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.


def SendEmail(to_email, subject, username):
        print("Sending Email Function")
        html_template = 'home/message.html'
        subject = subject
        from_email = settings.EMAIL_HOST_USER
        to_email = to_email
        print("to_email:",to_email)
        html_message = render_to_string(html_template, { 'username': username })
        message = EmailMessage(subject, html_message, from_email, [to_email])
        message.content_subtype = 'html' # this is required because there is no plain text email message
        message.send()
        print("Email Sent")
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
    print("Dashboard User:", request.user.nid)
    if request.user.is_authenticated:
        print("Sending Email")
        # import html message.html file
        # SendEmail("tanjimreza786@gmail.com", 'Welcome to PrimePark', request.user.name)
        return render(request, 'home/dashboard.html')
    else:
        return HttpResponse('Unauthorized')

def createslot(request):
    if request.method == 'POST':
        print("POST:",request.POST)
        print("Creating Slot...")

        NEWSPOT = Spot.objects.create(
            spot_id = request.POST.get('spot_id'),
            spot_area = request.POST.get('spot_area'),
            spot_road = request.POST.get('spot_road'),
            spot_house = request.POST.get('spot_house'),
            spot_number = request.POST.get('spot_number'),
            spot_maps_url = request.POST.get('spot_maps_url'),
            spot_desc = request.POST.get('spot_desc'),
            spot_owner = Users.objects.get(nid=request.user.nid),
        )
        NEWSPOT.save()
        print("New Spot Created")
        return redirect('table') 
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
        login_user(request, auth_user)
        SendEmail(to_email=user_email, subject='Welcome to PrimePark', username=user_name)
        print("auth_user:",auth_user)
        return redirect('dashboard')
    else:
        return render(request, 'home/signup.html')



def logout(request):
    print('Logout User:', request.user.nid)
    logout_user(request)
    return redirect('login')

def table(request): 
    return render(request, 'home/table.html')