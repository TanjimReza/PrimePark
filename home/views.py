from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
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
        

def index(request):
    return render(request, 'home/index.html')


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
    # print("Dashboard User:", request.user.nid)
    if request.user.is_authenticated:
        print("Dashboard User Type:", request.user.is_owner)

        return render(request, 'home/dashboard.html')
    else:
        return redirect('login')

def createslot(request):
    if request.user.is_authenticated:
        if request.user.is_owner == "S":
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
                
                NEWTIME = TimeSlots.objects.create(
                    spot = NEWSPOT
                )
                NEWTIME.save()        
                print("New Spot Created")
                return redirect('spots') 
            return render(request, 'home/createslot.html')
        else: 
            return redirect('unauthorized')
    else:
        return redirect('login')

def signup(request):
    if request.method == 'POST':
        pprint(request.POST)
        user_name = request.POST.get('name')
        user_nid = request.POST.get('nid')
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        user_contact = request.POST.get('contact')
        user_type = request.POST.get('is_owner')
        user = Users.objects.create(nid=user_nid, 
                                    password=user_password, 
                                    name=user_name, 
                                    email=user_email,
                                    contact=user_contact, 
                                    is_owner=user_type)
        user.save()
        messages.success(request, 'User created successfully')
        user.set_password(user_password)
        user.save()
        
        print("NEW USER:",user)
        #! Owner Creation Part
        if user_type == 'S':
            print("Creating Owner...")
            owner = SpotOwner.objects.create(user=user, 
                                             balance=0,
                                             )
            owner.save()
            print("Owner Created")
            return redirect('login')
        
        if user_type == 'D':
            print("Creating Driver...")
            driver = Drivers.objects.create(user=user)
            driver.save()
            print("Driver Created")
        
        if user_type == "R":
            print("Creating Renter...")
            renter = Rentee.objects.create(user=user)
            renter.save()
            print("Renter Created")
        
        
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

def spots(request): 
    
    ALL_SPOTS = Spot.objects.all()
    print(ALL_SPOTS)
    ALL_SPOTS = [spot for spot in ALL_SPOTS]
    ALL_TIMES = []
    for spot in ALL_SPOTS:
        print("Spot:",spot)
        slots = TimeSlots.objects.get(spot=spot)
        fields = slots._meta.get_fields()
        lst = []
        for field in fields:
            lst.append(field.value_from_object(slots))
        print("----")   
        lst = lst[2:]
        spot.spot_times = lst
        spot.save()
    context = {
        'ALL_SPOTS': ALL_SPOTS,
    }
    
    return render(request, 'home/spots.html',context=context)

def bookslot(request,id=""):
    spot = Spot.objects.get(spot_id=id)
    spot_timings = TimeSlots.objects.get(spot=spot)
    already_slots_data = []
    already_slots_data.append(spot_timings.slot_1)
    already_slots_data.append(spot_timings.slot_2)
    already_slots_data.append(spot_timings.slot_3)
    already_slots_data.append(spot_timings.slot_4)
    print("Already Slots:",already_slots_data)
    
    # print (spot.spot_slots)

    if request.method == 'POST':
        print("POST:",request.POST)
        print("Booking Slot...")
        post_request_slots = request.POST.getlist('booked_slots')
        print(post_request_slots)
        
        for i, time in enumerate(post_request_slots):
            if time in already_slots_data:
                if time == "9:00AM-11:00AM":
                    spot_timings.slot_1 = "Booked"
                    spot_timings.save()
                    already_slots_data[0] = "Booked"
                if time == "11:00AM-1:00PM":
                    spot_timings.slot_2 = "Booked"
                    spot_timings.save()
                    already_slots_data[1] = "Booked"
                if time == "1:00PM-3:00PM":
                    spot_timings.slot_3 = "Booked"
                    spot_timings.save()
                    already_slots_data[2] = "Booked"
                    
                if time == "3:00PM-5:00PM":
                    spot_timings.slot_4 = "Booked"
                    spot_timings.save()
                    already_slots_data[3] = "Booked"
        
        spot.spot_times = already_slots_data
        spot.save()
        
        print("Final Slots:",already_slots_data)
        
        
        
        
    context = {
        'id' : id,
        'spot': spot,
    }
    return render(request, 'home/bookslot.html',context=context)

def drivers(request):
    
    ALL_DRIVERS = Drivers.objects.all()
    context = {
        'ALL_DRIVERS': ALL_DRIVERS,
    }
    return render(request, 'home/drivers.html',context=context)


def unauthorized(request):
    return render(request, 'home/unauthorized.html')


def driverdashboard(request):
    print("here")
    if request.method == "POST":
        print(request.POST)
        driver = Drivers.objects.get(user=request.user)
        driver.driver_id = request.POST.get('license')
        driver.driver_area = request.POST.get('city')    
        driver.driver_about_me = request.POST.get('aboutyou')
        driver.driver_experience = request.POST.get('exp')
        driver.driver_contact = request.POST.get('contact')
        driver.save()
        print("Driver Updated")
        return redirect('driverdashboard')  
    
    driver = Drivers.objects.get(user=request.user)
    license = driver.driver_id
    area = driver.driver_area
    aboutyou = driver.driver_about_me
    expr = driver.driver_experience
    context = {
        'license': license,
        'area': area,
        'aboutyou': aboutyou,
        'expr': expr,
        'contact': driver.user.contact,
    }
    return render(request, 'home/driverdashboard.html',context=context)
        
    
    
    return render(request, 'home/driverdashboard.html')

def reviews(request,id=""):
    spot = Spot.objects.get(spot_id=id)
    
    if request.method == 'POST':
        print("POST:",request.POST)
        print("Reviewing Spot...")
        review = request.POST.get('review')
        print(review)
        existing_reviews = spot.spot_reviews
        existing_reviews += review 
        existing_reviews += "."
        spot.spot_reviews = existing_reviews
        spot.save()
        print("Spot Reviewed")
        return redirect('dashboard')
    
    context = {
        'spot': spot,
    }
    return render(request, 'home/reviews.html',context=context)

def allreviews(request):
    ALL_SPOTS = Spot.objects.all()
    context = {
        'ALL_SPOTS': ALL_SPOTS,
    }
    return render(request, 'home/allreviews.html',context=context)


def makepayment(request):
    if request.method == 'POST':
        print("POST:",request.POST)
        user = Users.objects.get(nid=request.user.nid)
        user.user_balance = user.user_balance + int(request.POST.get('amount'))
        user.save()
        return redirect('dashboard')
    return render(request, 'home/makepayment.html')

def driverportfolio(request,id=""):
    driver = Drivers.objects.get(driver_id=id)
    license = driver.driver_id
    area = driver.driver_area
    aboutyou = driver.driver_about_me
    expr = driver.driver_experience
    contact = driver.driver_contact
    
    # contact = Users.objects.get(user=driver.user)
    
    # print(contact)
    context = {
        'license': license,
        'area': area,
        'aboutyou': aboutyou,
        'expr': expr,
        'contact': contact,
    }
    
    return render(request, 'home/driverportfolio.html',context=context)