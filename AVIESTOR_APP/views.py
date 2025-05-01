from django.shortcuts import render, HttpResponsePermanentRedirect, redirect
from django.contrib.auth import authenticate, login as auth_user, logout 
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
import random
import http.client
from django.conf import settings

def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')

def loginuser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        user = authenticate(email=email, phone=phone)
        if user is None:
            messages.error(request, 'INVALID EMAIL')
            return HttpResponsePermanentRedirect('login.html')
        if user is None:
            messages.error(request, "INVALID PHONE NUMBER")
            return HttpResponsePermanentRedirect(request, 'login.html')
        else:
            auth_user(request, user)
            return render(request, '#')
    return render(request, 'login.html')

# def register(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         name = request.POST.get('name')
#         mobile = request.POST.get('mobile')

#         check_user = User.objects.filter(email=email).first()
#         check_profile = Profile.objects.filter(mobile=mobile).first()

#         if check_user or check_profile: 
#             context = {'message': 'user already exists', 'class': 'alert alert-danger'}
#             return render(request, 'register.html', context)
        
#         user = User(email=email, first_name=name)  # Ensure username is excluded
#         user.is_active = True  # Ensure the user is active
#         user.save()

#         otp = str(random.randint(1000, 9999))
#         profile_instance = Profile(user=user, mobile=mobile, otp=otp)
#         profile_instance.save()
#         send_otp(mobile, otp)
#         request.session['mobile'] = mobile
#         return render(request, 'otp.html')
#     return render(request, 'refdemo.html')

# def register(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         mobile = request.POST.get('mobile')

#         # Check if user with this email or mobile already exists
#         check_user = User.objects.filter(email=email).first()
#         check_profile = Profile.objects.filter(mobile=mobile).first()

#         if check_user or check_profile:
#             context = {'message': 'User already exists', 'class': 'alert alert-danger'}
#             return render(request, 'refdemo.html', context)

#         # Since you're not using 'name', skip it. Ensure `username` is required.
#         user = User(username=email, email=email)  # We're using email as username
#         user.is_active = True  # Make sure user is active
#         user.save()

#         # Generate OTP for the mobile number
#         otp = str(random.randint(1000, 9999))
#         profile_instance = Profile(user=user, mobile=mobile, otp=otp)
#         profile_instance.save()

#         # Send OTP to mobile
#         send_otp(mobile, otp)

#         # Save mobile to session for OTP verification
#         request.session['mobile'] = mobile
#         return render(request, 'otp.html')

#     # Render the registration form if GET request
#     return render(request, 'refdemo.html')

def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid user')
            return HttpResponsePermanentRedirect('/login/')
        user=authenticate(username=username , password=password)
        if user is None:
            messages.error(request,'Invalid password')
            return HttpResponsePermanentRedirect('/login/')
        else:
            auth_user(request,user)
            return HttpResponsePermanentRedirect('/home/')
    return render(request , 'login.html')

def register(request):
    if request.method=='POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        # confirm_password=request.POST.get('confirm-password')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'User already Exists')
            return HttpResponsePermanentRedirect('/signup/')
        user=User.objects.create_user(first_name = firstname , last_name = lastname , email=email , username=username )
        user.set_password(password)
        user.save()
        messages.info(request,'User create sucessfully')
        return HttpResponsePermanentRedirect('/login/')
    return render(request , 'refdemo.html')


def send_otp(mobile, otp):
    conn = http.client.HTTPSConnection("control.msg91.com")
    authkey = settings.AUTH_KEY
    headers = {
        'Content-Type': "application/JSON",
        'content-type': "application/json",
    }
    url = "http://control.msg91.com/api/sendotp.php?otp=" + otp + "&sender=ABCmessage" + 'your otp is ' + otp + '&mobile' + mobile + '&authkey=' + authkey + '&country=91'
    
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return None

def otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        check_profile = Profile.objects.filter(mobile=mobile).first()
        if otp == check_profile.otp:
            return redirect('')
        else:
            context = {'message': 'Invalid OTP', 'class': 'alert alert-danger'}
    return render(request, 'otp.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')  # or wherever you want to send the user

def apple(request):
    return render(request, 'APPLE.html')

def Reliance(request):
    return render(request, 'Reliance.html')

def Aboutus(request):
    return render(request, 'About.html')
