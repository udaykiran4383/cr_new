from tablib import Dataset
import email
import os
from django.core.mail import send_mail
import random
from django.contrib.auth.decorators import login_required
import json
from django.dispatch import receiver
from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile, College, Student
from .serializers import UserSerializer
import pandas as pd
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, "user/index.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            auth_login(request, user)
            cuser = UserProfile.objects.all()
            data = {'cuser': cuser}
            return render(request, 'user/cpanel.html', data)
        else:
            messages.error(request, "Wrong Credentials")
            return render(request, "user/login.html")
    
    return render(request, "user/login.html")

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('index')

def signup(request):
    return render(request, "user/signup.html")


@login_required
def dashboard(request, id):
    main = User.objects.get(id=id)
    email = main.email
    try:
        user = UserProfile.objects.get(email=email)
        data = {'id': id, 'my': user}
        return render(request, 'user/dashboard.html', data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id': id, 'email': email}
        return render(request, 'user/profile.html', data)

def get_or_create_college(name, state, district):
    college, created = College.objects.get_or_create(name=name, district=district, state=state)
    return college, created

def add_college_to_json(state, district, new_college_name):
    file_path = os.path.join(settings.BASE_DIR,  'static', 'states_districts.json')

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'states': []}

    state_found = False
    for state_obj in data['states']:
        if state_obj['state'] == state:
            state_found = True
            district_found = False
            for district_obj in state_obj['districts']:
                if district_obj['name'] == district:
                    district_found = True
                    if 'colleges' not in district_obj:
                        district_obj['colleges'] = []
                    if new_college_name not in district_obj['colleges']:
                        district_obj['colleges'].append(new_college_name)
                    break
            if not district_found:
                state_obj['districts'].append({
                    'name': district,
                    'colleges': [new_college_name]
                })
            break

    if not state_found:
        data['states'].append({
            'state': state,
            'districts': [{
                'name': district,
                'colleges': [new_college_name]
            }]
        })

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def add_college(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            state = data['state']
            district = data['district']
            new_college = data['new_college']

            file_path = os.path.join(settings.BASE_DIR, 'user_account', 'static', 'states_districts.json')
            try:
                with open(file_path, 'r') as file:
                    json_data = json.load(file)
            except FileNotFoundError:
                json_data = {'states': []}

            state_obj = next((s for s in json_data['states'] if s['state'] == state), None)
            if state_obj:
                district_obj = next((d for d in state_obj['districts'] if d['name'] == district), None)
                if district_obj:
                    if 'colleges' not in district_obj:
                        district_obj['colleges'] = []
                    if new_college not in district_obj['colleges']:
                        district_obj['colleges'].append(new_college)
                else:
                    state_obj['districts'].append({
                        'name': district,
                        'colleges': [new_college]
                    })
            else:
                json_data['states'].append({
                    'state': state,
                    'districts': [{
                        'name': district,
                        'colleges': [new_college]
                    }]
                })

            with open(file_path, 'w') as file:
                json.dump(json_data, file, indent=4)
            
            return JsonResponse({'status': 'success', 'message': f"College '{new_college}' added successfully to {state}, {district}"}, status=200)
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def updateprofile(request, id):
    if request.method == 'POST':
        try:
            li = range(1000, 5000)
            cr_global = random.sample(li, 1)
            referral = random.sample(li, 1)
            ref = "REF" + str(referral[0])
            myid = request.POST['myid']
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            whatsapp = request.POST['whatsapp']
            cr = "CR 24 " + str(cr_global[0])
            year = request.POST['year']
            bonus = request.POST['bonus']

            state = request.POST['state']
            district = request.POST['district']
            college_name = request.POST['college']
            if college_name == 'other':
                new_college_name = request.POST['new_college']
                college, created = get_or_create_college(new_college_name, state, district)
                if created:
                    add_college_to_json(state, district, new_college_name)
            else:
                try:
                    college = College.objects.get(name=college_name, district=district, state=state)
                except College.DoesNotExist:
                    return render(request, 'user/profile.html', {'error': 'College not found. Please enter a new college.'})

            cr_id = cr
            info = UserProfile(
                cr_id=cr_id, name=name, email=email, phone=phone, whatsapp=whatsapp, 
                year=year, ref=ref, bonus_ref=bonus, state=state, district=district, college=college
            )
            info.save()
            
            send_registration_email(name, cr, ref, email)

            return redirect('dashboard', id=myid)
        except Exception as e:
            print(f"Error occurred: {e}")
            return render(request, 'user/profile.html', {'error': str(e)})
    return render(request, 'user/profile.html')


def send_registration_email(name, cr, ref, email):
    subject = "Congratulations for enrolling in CR Program of Abhyuday IIT Bombay"
    message = f"""Congratulations {name}!! \n
    You have successfully registered in the College Representative Internship Program 2022-23 of Abhyuday, IIT Bombay! We welcome you to the Abhyuday family! \n
    Your College Representative ID for your tenure as a CR will be {cr}. \n
    You would soon receive your Coding Ninjas discount coupons! \n
    You can share the following referral code with your friends from your college to form a team and with other friends to earn more points for your team. \nReferral Code - {ref} \n
    Lots of good wishes for your new endeavors with Abhyuday, IIT Bombay. \n"Do what you can, with what you have, where you are." -Theodore Roosevelt \n
    Regards, \nAbhyuday"""
    send_mail(subject, message, 'cr.abhyuday.iitbombay@gmail.com', [email])

@login_required
def yourprofile(request, id):
    main = User.objects.get(id=id)
    email = main.email
    try:
        user = UserProfile.objects.get(email=email)
        data = {'id': id, 'user': user}
        return render(request, 'user/inner_profile.html', data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id': id, 'email': email}
        return render(request, 'user/profile.html', data)
@login_required
def myprofile(request, id):
    main = User.objects.get(id=id)
    email = main.email
    try:
        if request.method == 'POST':
            crid = request.POST['crid']
            name = request.POST['name']
            phone = request.POST['phone']
            whatsapp = request.POST['whatsapp']
            year = request.POST['year']

            user = UserProfile.objects.get(email=email)
            user.name = name
            user.phone = phone
            user.whatsapp = whatsapp
            user.year = year
            user.save()

        data = {'id': id, 'user': user}
        return render(request, 'user/inner_profile.html', data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id': id, 'email': email}
        return render(request, 'user/profile.html', data)

def google(request):
    objs = User.objects.all()
    data = []

    for obj in objs:
        data.append({
            "Name": obj.username,
            "Email": obj.email,
        })

    pd.DataFrame(data).to_excel('google.xlsx')
    return JsonResponse({
        'status': 200
    })

def taskmail(request):
    objs = UserProfile.objects.all()
    for obj in objs:
        sub = "Task 1 is released"
        msg = """Greetings from Abhyuday, IIT Bombay! \n
Hope you are doing well! \n
We would like to inform you about the release of the new task.\n
Please log in on the CR Portal.
Use the following URL to see the task on the dashboard - https://cr.abhyudayiitb.org/  \n
Please read the instructions carefully and start planning the execution of the task with the help of your mentor as soon as possible. \n
Make a habit of saying yes in your life, and embrace every new opportunity. You are certain to receive peace, joy, and fulfilment in life.  \n
Wish you all the best for the completion of the given task! \n
Regards,
Team Abhyuday
"""
        send_mail(
            sub, msg, 'cr.abhyuday.iitbombay@gmail.com', [obj.email]
        )

    return HttpResponse("Done")

