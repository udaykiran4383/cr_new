from pickle import TRUE
from django.dispatch import receiver
from django.shortcuts import redirect, render , HttpResponse ,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from yaml import serialize
from . models import UserProfile , Invite , Team
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.core import serializers

# Create your views here.

def index(request):
    return render(request , "user/index.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password = pass1)

        if user is not None:
            auth_login(request, user)
            cuser = UserProfile.objects.all()
            team = Team.objects.all()
            data = {
                'cuser':cuser,
                'team':team
            }
            return render(request, 'user/cpanel.html',data)

        else:
            messages.error(request, "Wrong Credentials")
            return render(request , "user/login.html")
    
    return render(request , "user/login.html")

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged Out Successfully!")

    return redirect('index')


def signup(request):
    return render(request , "user/signup.html")

cr_global = 1001
gmail = "test"
def confirm(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        request.session['email'] = email
        global gmail
        gmail = email
        alert =0
        objs = UserProfile.objects.all()
        for obj in objs:
            if obj.email == email:
                alert = 1
        if alert == 0:
            global cr_global
            cr_global += 1
            sub = "Congratulations for enrolling in CR Program of Abhyuday IIT Bombay"
            msg = "Congratulations " + name + " your cr id is CR" + str(cr_global)
            request.session['cr_id']="CR"+str(cr_global)
            send_mail(
                sub, msg, 'abhyudayiitb2022@gmail.com',[email]
            )
            return redirect('profile')
            
        else:
            return redirect('dashboard')
        

def dashboard(request):
    id =0
    cr_id=0
    objs = UserProfile.objects.all()
    for obj in objs:
        global gmail
        if obj.email == gmail:
            id = obj.id
            cr_id = obj.cr_id
    data={'id':id,'cr_id':cr_id}
    return render(request, 'user/dashboard.html',data)


def profile(request):
    return render(request ,'user/profile.html' )
            

def updateprofile(request ):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.session['email']
        phone = request.POST['phone']
        whatsapp = request.POST['whatsapp']
        state = request.POST['state']
        year = request.POST['year']
        college = request.POST['college']
        city = request.POST['city']
        sop = request.POST['sop']
        cr_id = request.session['cr_id']
        info = UserProfile(cr_id=cr_id,name= name,email=email,phone=phone, whatsapp = whatsapp, state=state, year=year,college=college,city=city,sop=sop)
        info.save()
        

    return redirect('user/dashboard')

def leaderboard(request):
    id =0
    cr_id=0
    objs = UserProfile.objects.all()
    for obj in objs:
        global gmail
        if obj.email == gmail:
            id = obj.id
            cr_id = obj.cr_id
    
        team.team_status = True
        team.save()
    else:
        team.team_status = False
        team.save() 

    data1 = UserProfile.objects.all().order_by('-points')
    print(data1)

    user = {
        "user": data1,'id':id,'cr_id':cr_id
    }
    
    return render(request, 'user/leaderboard.html' , user)

def teamLeaderboard(request):
    id =0
    cr_id=0
    obj = UserProfile.objects.get(email= gmail)
    team = Team.objects.filter(team_status = True)
    id = obj.id
    cr_id = obj.cr_id
    data={'id':id,'cr_id':cr_id,'teams':team}
    return render(request, 'user/team_board.html',data)

def team(request):
    id =0
    cr_id=0
    obj = UserProfile.objects.get(email= gmail)
    team = Team.objects.filter(team_status = True)
    id = obj.id
    cr_id = obj.cr_id
    if request.method == "POST":
        teamname = request.POST['teamname']
        leader = request.POST['teamleader']
        cr_id1 = request.POST['crid1']
        member2 = request.POST['member2']
        cr_id2 = request.POST['crid2']
        member3 = request.POST['member3']
        cr_id3 = request.POST['crid3']
        member4 = request.POST['member4']
        cr_id4 = request.POST['crid4']
        team = Team(teamname = teamname, leader=leader,crid1 = cr_id1,member2 = member2,crid2=cr_id2,member3=member3, crid3 = cr_id3,member4=member4,crid4=cr_id4)
        team.save()
        objs = UserProfile.objects.all()
        for obj in objs:
            if obj.cr_id == cr_id1:
                id1 = obj.id
            if obj.cr_id == cr_id2:
                id2 = obj.id
                invite2 = Invite(sender_name = leader, sender= id1, sender_cr_id = cr_id1 , receiver = id2)
                invite2.save()
            if obj.cr_id == cr_id3:
                id3 = obj.id
                invite3 = Invite(sender_name = leader, sender= id1, sender_cr_id = cr_id1 ,receiver = id3)
                invite3.save()   
            if obj.cr_id == cr_id4:
                id4 = obj.id
                invite4 = Invite(sender_name = leader, sender= id1,sender_cr_id = cr_id1 , receiver = id4)
                invite4.save()
    
    team ={}
    objs = Team.objects.all()
    for obj in objs:
        if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
            team = obj

    teamreg = Invite.objects.filter(sender_cr_id = team.crid1)
    count = 0
    for obj in teamreg:
        if obj.status == True:
            count= count +1

    if count == 3:
        team.team_status = True
        team.save()
    else:
        team.team_status = False
        team.save() 

    data ={
        'teamreg':teamreg,
        'id':id,'cr_id':cr_id,'teamname':team.teamname,'leader':team.leader,'team_status':team.team_status
    }
    return render(request , 'user/team.html' , data)

def invite(request , id):
    id =0
    cr_id=0
    obj = UserProfile.objects.get(email= gmail)
    id = obj.id
    cr_id = obj.cr_id
    
    user = UserProfile.objects.get(id= id)
    invite_data = Invite.objects.filter(receiver = id)
    team ={}
    objs = Team.objects.all()
    for obj in objs:
        if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
            team = obj
    in_team = team.team_status
    invite = {
        "invite": invite_data,
        "name":  user.name,'id':id,'cr_id':cr_id,
        "in_team": in_team
    }
    
    return render(request, 'user/invite.html',invite)

def accept(request , id , sender_id):
    team = Invite.objects.get(receiver = id , sender= sender_id)
    user = UserProfile.objects.get(id = id)
    user.in_team = True
    team.status = True
    team.save()
    user.save()
    return HttpResponse("it worked")

def task1(request):
    id =0
    cr_id=0
    obj = UserProfile.objects.get(email= gmail)
    id = obj.id
    cr_id = obj.cr_id

    if request.method == "POST":
        proof = request.POST['proof']
        user = UserProfile.objects.get(id = id)
        if user.in_team == True:
            team ={}
            objs = Team.objects.all()
            for obj in objs:
                if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
                    team = obj
            team.proof = proof
            team.save()
        else:
            return redirect('team')
    user = UserProfile.objects.get(id = id)
    if user.in_team == True:
        team ={}
        objs = Team.objects.all()
        for obj in objs:
            if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
                team = obj
        
    data={'id':id,'cr_id':cr_id,'task1':team.task1_status}
    return render(request , 'user/task1.html' ,data)

def point(request , id):
    team = Team.objects.get(id = id)
    data = {
        'team':team,
    }
    
    if request.method == 'POST':
        point = request.POST['point']
        team.teampoint = point
        team.save()
        

    return render(request, 'user/point.html' , data)