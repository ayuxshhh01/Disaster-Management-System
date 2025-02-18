from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.core import serializers
from django.http import JsonResponse
import http.client
from .forms import SubscribeForm
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import firestore,auth
from urllib.parse import quote_plus
from django.core.mail import send_mail
import requests
import threading
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import login, authenticate
from .models import MinistryNewss
# from django.http import JsonResponse
# from .models import Hospital

if not firebase_admin._apps:
    cred = credentials.Certificate('news/credentials.json')
    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://console.firebase.google.com/u/0/project/rjkta-e0ae5/database/rjkta-e0ae5-default-rtdb/data/~2F?fb_gclid=CjwKCAiAneK8BhAVEiwAoy2HYW6kgF9cZ--Kq0L8fkns2K70zMvg_hw_IfxbAA56xS2KOaBAM-isRBoC7OYQAvD_BwE'  # Replace with your database URL
})
db = firestore.client()

#Display-Database
doc_ref = db.collection(u'RealNews')
snapshot = doc_ref.get()
news = db.collection('RealNews').order_by('date',direction=firestore.Query.DESCENDING).limit(30).stream()
l2 = []
for n in news:
    l1 = []
    data = n.to_dict()
    date = data['date']
    headline = data['headline']
    image_url = data['imageurl']
    description = data['description']
    share_link = quote_plus(data['headline'])
    l1.append(date)
    l1.extend((headline,description,share_link,image_url))
    l2.append(l1)
k = pd.DataFrame(l2,columns=['date','headline','description','share_link','image_url'])

def homepage(request):
    #Ministry-news
    queryset = MinistryNewss.objects.all().order_by('-date')
    print(queryset)
        #Real-time Updation
    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(doc_snapshot, changes, read_time):
        email_send=[]

        for d in doc_snapshot:
            # print(d.to_dict())
            headline='NO'
            doc = d.to_dict()
            headline = doc.get('headline', "NO headline available")  # Ensure headline always has a value
            description = doc.get('description', "NO description available")  # Safe fallback value

        print(f'Received document snapshot: {headline}')
        #Retrieval of Users:- 
        doc_email = db.collection('Users').stream()
        for d in doc_email:
            email_send = []
            data = d.to_dict()
            email = data.get('email', None)  # Retrieve email safely
            contact = data.get('contact', "")
            if email:
                 email_send.append(email)            #appending-it-to-the-email-list
            
            #SENDING SMS TO EACH USER 
            headline='NO headline available'
            message = headline
            url = "https://www.fast2sms.com/dev/bulk"
            if len(contact) > 10:
                number = contact[3:]
            else:
                number = contact
            payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers="+number
            headers = {
            'authorization': "FWLraiHjfoSUGcBeJuOT9sQNCdPbgpw4EXI63yD720ntMA8K51WV1Kw5NTikXExzIA6y74vHJSpClFMb",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text) 

        #SENDING EMAILS TO EACH USER

        if email_send:
            send_mail(headline,description,'ayushdube596@gmail.com',email_send,fail_silently=False)

        callback_done.set()
    doc_ref = db.collection(u'RealNews')

    # WATCHES DOCUMENT FOR ANY CHANGE IN DOCUMENTS
    doc_watch = doc_ref.on_snapshot(on_snapshot)

    message = ""
    #Subscribe-user
def homepage(request):
    form = SubscribeForm()
    message = ""  # Ensure 'message' is always defined

    # Ensure 'context1' is always initialized
    context1 = dict(
        data=[],  # Set a default value for 'data' if 'k' is undefined
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

        # Update context3 with the latest message
        context3 = {'mess': message}

    return render(request, 'news/base.html', {'context1': context1, 'context2': context2, 'context3': context3})


#SOS - BUTTON for Ambulance
def Relief_help(request):

    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        hospital = request.POST['hospital']
        user_latitude = request.POST['lat']
        user_longitude = request.POST['lon']


        print(name)
        print(contact)
        print(hospital)
        print(user_longitude,user_longitude)
    
        url = "https://www.fast2sms.com/dev/bulkV2"
        message = 'Hi, I am '+name + 'I need help! My location is ('+user_latitude + ',' + user_longitude + ')'
        number = '9172781316'
        payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers="+number
        headers = {
        'authorization': "cTJUj4kuqpHf1LWAyvsKl0Qog6EMtd2iCra3mVSNXh7nIGw8Ze8cQTvdmW1rDyk3qlxVA5bIO9hBtG7F",
        'Content-Type':"application/json",
        'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text) 

    return render(request, 'news/base.html')

#SOS - BUTTON For FIrst-Aid
def Relief_help2(request):

    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        ngo = request.POST['ngo']
        injury = request.POST['injury']
        user_latitude = request.POST['lat']
        user_longitude = request.POST['lon']


        print(name)
        print(contact)
        print(ngo)
        print(user_longitude,user_longitude) 

        url = "https://www.fast2sms.com/dev/bulkV2"
        message = 'Hi, I am '+name + 'I need help! My location is ('+user_latitude + ',' + user_longitude + ')'
        number = contact
        payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers="+number
        headers = {
        'authorization': "cTJUj4kuqpHf1LWAyvsKl0Qog6EMtd2iCra3mVSNXh7nIGw8Ze8cQTvdmW1rDyk3qlxVA5bIO9hBtG7F",
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text) 

    return render(request, 'news/base.html')

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
# def hospital_locations(request):
#     hospitals = Hospital.objects.all()
#     data = [{"name": h.name, "lat": h.location.y, "lng": h.location.x} for h in hospitals]
#     return JsonResponse(data, safe=False)
# from django.shortcuts import render

# def map_view(request):
#     return render(request, 'news/base.html')
# from django.shortcuts import render
# import requests

from django.http import JsonResponse

def prediction_view(request):
    try:
        # Fetch weather data
        weather_url = "http://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid=5c6621d889d5bb4d009983274a99c9fe"
        weather_data = requests.get(weather_url).json()

        # Fetch earthquake data
        earthquake_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson"
        earthquake_data = requests.get(earthquake_url).json()

        # Prepare response
        response_data = {
            'weather': weather_data,
            'earthquakes': earthquake_data.get("features", [])
        }

        return JsonResponse(response_data)  # ✅ Return JSON, NOT a template

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page or other destination
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'news/base.html', {'form': form})
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'news/base.html')

