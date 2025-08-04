from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.core import serializers
from django.http import JsonResponse
import http.client
from .forms import SubscribeForm
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore,auth
from urllib.parse import quote_plus
from django.core.mail import send_mail
import requests
import threading
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import login, authenticate
from .models import MinistryNewss
from django.http import JsonResponse
# from .models import Hospital
from google.cloud import firestore
from django.contrib.auth import logout
from django.shortcuts import redirect
import requests
from twilio.rest import Client
from django.conf import settings
import os
from google.cloud import firestore
from google.auth.transport.requests import Request
from google.auth import exceptions

# Set the path to your credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\ayush\OneDrive\Desktop\project A\ResponseWebsite\website\news\credentials.json"

# Now initialize the Firestore client
try:
    db = firestore.Client()
    print("Firestore client initialized successfully.")
except exceptions.DefaultCredentialsError as e:
    print(f"Error: {e}")





if not firebase_admin._apps:
    cred = credentials.Certificate('news/credentials.json')
    firebase_admin.initialize_app(cred)

db = firestore.Client()
  # ✅ firestore client, not db from realtime





def homepage(request):
    query = MinistryNewss.objects.all().order_by('-date')  # This fetches news from your model
    form = SubscribeForm()
    message = ""

    context1 = dict(
        data=query,  # Send actual queryset here
        columns=['date', 'headline', 'description', 'share_link']
    )

    context2 = {'form': form}
    context3 = {'mess': message}

    if request.method == 'POST':
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        data = {'name': request.POST.get('name'), 'email': email, 'contact': contact}
        form = SubscribeForm(request.POST)

        if form.is_valid():
            doc = db.collection(u'Users').where(u'contact', '==', contact).get()
            if doc:
                message = 'Contact exists! Re-enter New Details!'
            else:
                message = "SUBSCRIPTION is completed!!"
                db.collection('Users').add(data)
        else:
            message = "INVALID INPUT DETAILS!!"
        context3 = {'mess': message}

    return render(request, 'news/base.html', {
        'context1': context1,
        'context2': context2,
        'context3': context3,
        'query': query  # Add this so you can access news directly in template
    })



#SOS - BUTTON for Ambulance


from django.shortcuts import render
from twilio.rest import Client

def Relief_help(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        contact = request.POST.get('contact', '')
        hospital = request.POST.get('hospital', '')
        user_latitude = request.POST.get('lat', '')
        user_longitude = request.POST.get('lon', '')

        # Twilio Credentials
        account_sid = 'AC0808c6c8a16d734ff872e0fbc796c682'
        auth_token = '8f818d437a8419f6ae61254671cbd738'
        twilio_number = '+17439629205'
        destination_number = '+919172781316'  # Must be verified if using trial account

        message_body = (
            f"Hi, I am {name}. I need help from {hospital}! "
            f"My location is ({user_latitude}, {user_longitude}). Contact: {contact}"
        )

        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=destination_number
            )
            print("✅ Message sent successfully. SID:", message.sid)
        except Exception as e:
            print("❌ Failed to send SMS:", repr(e))

    return render(request, 'news/base.html')




#SOS - BUTTON For FIrst-Aid
from django.shortcuts import render
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def rel_help2(request):
    name = request.POST.get('name')
    ngo = request.POST.get('ngo')
    injury = request.POST.get('injury')
    lat = request.POST.get('lat')
    lon = request.POST.get('lon')

    message_body = f"🚨 SOS Alert 🚨\nName: {name}\nInjury: {injury}\nNearest NGO: {ngo}\nLocation: https://maps.google.com/?q={lat},{lon}"

    try:
        # Replace these with your Twilio credentials
        account_sid = "AC0808c6c8a16d734ff872e0fbc796c682"
        auth_token = "8f818d437a8419f6ae61254671cbd738"
        from_number = "+17439629205"
        to_number = "+919172781316"

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )

        return JsonResponse("success", safe=False)

    except Exception as e:
        print("Twilio error:", e)
        return JsonResponse("Failed to send SOS", safe=False)


def message(request):
    
    return render(request, 'news/base.html')


def test_email(request):
    doc_ref = db.collection(u'RealNews')
    snapshot = doc_ref.get()
    news = db.collection('RealNews').order_by('date',direction=firestore.Query.DESCENDING).limit(1).stream()
    for n in news:
        data = n.to_dict()

    title = data['headline']
    body = data['description']

    send_mail(title,body,'ayushdube596@gmail.com',['ayushdube@gmail.com'],fail_silently=False)
    return render(request,'news/base.html')




def earthquake(request):
    return render(request,'news/earthquake.html')

def storms(request):
    return render(request,'news/storms.html')

def floods(request):
    return render(request,'news/floods.html')

def wildfire(request):
    return render(request,'news/wildfire.html')

def pandemic(request):
    return render(request,'news/pandemic.html')

def violence(request):
    return render(request,'news/violence.html')

def first_aid(request):
    return render(request,'news/first-aid.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  # change to your desired redirect URL
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'news/base.html')

