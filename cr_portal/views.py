import email
from pickle import TRUE
# from tkinter.font import BOLD
from django.dispatch import receiver
from django.shortcuts import redirect, render , HttpResponse ,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from numpy import single
from yaml import serialize
from . models import UserProfile , Invite , Team, Blog
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.core import serializers
import random

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

# referral = 5423
# cr_global = 1001
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
            li=range(0,5000)
            cr_global = random.sample(li,1)
            referral = random.sample(li,1)
            cr=cr_global[0]
            ref=referral[0]
            print(cr)
            print(ref)
            sub = "Congratulations for enrolling in CR Program of Abhyuday IIT Bombay"
            msg = """Congratulations """ + name+"""!! \n
You have successfully registered in the College Representative Internship Program 2022-23 of Abhyuday, IIT Bombay! We welcome you to the Abhyuday family! \n
Your College Representative ID for your tenure as a CR will be CR""" +str(cr)+""". \n
You can share the following referral code with your friends from your college to form a team and with other friends to earn more points for your team. \nReferral Code - REF""" +str(ref)+ """\n
Lots of good wishes for your new endeavours with Abhyuday, IIT Bombay. \n"Do what you can, with what you have, where you are." -Theodore Roosevelt \n
Regards, \nAbhyuday"""
            # "Congratulations " + name + " your cr id is CR" + str(cr) + " Your referral code is REF" + str(ref)
            request.session['cr_id']="CR"+ str(cr)
            request.session['ref']="REF"+ str(ref)

            send_mail(
                sub, msg, 'lasttest940@gmail.com',[email]
            )
            return redirect('profile')
            
        else:
            return redirect('dashboard')
        

def dashboard(request):
    id =0
    cr_id=0
    ref=0
    objs = UserProfile.objects.all()
    for obj in objs:
        global gmail
        if obj.email == gmail:
            id = obj.id
            cr_id = obj.cr_id
            ref = obj.ref
    data={'id':id,'cr_id':cr_id , 'ref':ref}
    return render(request, 'user/dashboard.html',data)


def profile(request):
    return render(request ,'user/profile.html' )
            

def updateprofile(request ):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.session['email']
        ref = request.session['ref']
        phone = request.POST['phone']
        whatsapp = request.POST['whatsapp']
        state = request.POST['state']
        year = request.POST['year']
        college = request.POST['college']
        city = request.POST['city']
        sop = request.POST['sop']
        cr_id = request.session['cr_id']
        bonus = request.POST['bonus']
        info = UserProfile(cr_id=cr_id,name= name,email=email,phone=phone, whatsapp = whatsapp, state=state, year=year,college=college,city=city,sop=sop,ref=ref,bonus_ref=bonus)
        info.save()
        # profile = UserProfile.objects.get(email = gmail)
        # id = profile.id
    return redirect('dashboard')

def leaderboard(request):
    id =0
    cr_id=0
    obj = UserProfile.objects.get(email= gmail)
    team = Team.objects.filter(team_status = True).order_by('-teampoint')
    id = obj.id
    cr_id = obj.cr_id
    mypoint = obj.points
    inteam = obj.in_team

    data1 = UserProfile.objects.filter( in_team = False ).order_by('-points')

    myrank =0
    for idx, obj in enumerate(data1):
        if obj.cr_id == cr_id:
            myrank = idx + 1

    team_rank =0
    for idy, obj in enumerate(team):
        if (obj.crid1 == cr_id) or (obj.crid2 == cr_id) or (obj.crid3 == cr_id) or (obj.crid4 == cr_id):
            team_rank = idy + 1
            
    # print(data1)
    
    team_point =0
    objs = Team.objects.all()
    for obj in objs:
        if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
            team_point = obj.teampoint

    user = {
        "user": data1,'id':id,'cr_id':cr_id,'teams':team,'rank':myrank , 'teamrank':team_rank, 'teampoint':team_point , 'mypoint':mypoint , 'inteam':inteam
    }

    
    return render(request, 'user/leaderboard.html' , user)

# def teamLeaderboard(request):
#     id =0
#     cr_id=0
#     obj = UserProfile.objects.get(email= gmail)
#     team = Team.objects.filter(team_status = True)
#     id = obj.id
#     cr_id = obj.cr_id
#     data={'id':id,'cr_id':cr_id,'teams':team}
#     return render(request, 'user/team_board.html',data)

def team(request):
    
    cr_id=0
    obj = UserProfile.objects.get(email= gmail)
    team = Team.objects.filter(team_status = True)
    name = obj.name
    cr_id = obj.cr_id
    id = obj.id
    inteam = obj.in_team
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
        objes = UserProfile.objects.all()
        member = UserProfile.objects.get(id =id)
        member.in_team = True
        member.save()
        invite2 = Invite(sender_name = leader, sender= id, sender_cr_id = cr_id , receiver = cr_id2)
        invite2.save()
        invite3 = Invite(sender_name = leader, sender= id, sender_cr_id = cr_id ,receiver = cr_id3)
        invite3.save()   
        invite4 = Invite(sender_name = leader, sender= id,sender_cr_id = cr_id , receiver = cr_id4)
        invite4.save()
        team.save()
        
    
    team =0
    objs = Team.objects.all()
    for obj in objs:
        if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
            team = obj

    objes = Invite.objects.all()
    temp =0
    for obj in objes:
        if obj.receiver == cr_id:
            temp =1

    print(temp)
    cr= ""
    for m in cr_id:
        if m.isdigit():
            cr = cr + m
    
    numcr = int(cr)
    # counter =0
    # objes = Invite.objects.all()
    # for obj in objes:
    #     counter += counter
    
    # if counter == 0:
    #     data ={
    #         'name':name,'cr_id':cr_id,
    #     }
    #     return render(request , 'user/team.html',data )
    
    # else:

    if team !=0:
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
        print(count)
        data ={
            'teamreg':teamreg,
            'name':name,'cr_id':cr_id,'id':id,
            'teamname':team.teamname,'leader':team.leader,'team_status':team.team_status,'leader_id':team.crid1,'cr':numcr , 'temp':temp ,'inteam':inteam
        }
        return render(request , 'user/team.html',data )
    else:
        data ={
            # 'teamreg':teamreg,
            'name':name,'cr_id':cr_id,'id':id,'temp':temp ,'inteam':inteam
            # 'teamname':team.teamname,'leader':team.leader,'team_status':team.team_status,'leader_id':team.crid1
        }
        return render(request , 'user/team.html',data )



def invite(request , id):
    id =0
    cr_id=0
    obj = UserProfile.objects.get(email= gmail)
    id = obj.id
    cr_id = obj.cr_id
    
    user = UserProfile.objects.get(id= id)
    invite_data = Invite.objects.filter(receiver = cr_id)

    cr= ""
    for m in cr_id:
        if m.isdigit():
            cr = cr + m
    
    numcr = int(cr)
    # team ={}
    # objs = Team.objects.all()
    # for obj in objs:
    #     if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
    #         team = obj
    # in_team = team.team_status
    invite = {
        "invite": invite_data,
        "name":  user.name,'id':id,'cr_id':cr_id,'cr':numcr
        # "in_team": in_team
    }
    
    return render(request, 'user/invite.html',invite)

def accept(request ,id ,cr, sender_id):
    fullcr= "CR"+str(cr)
    
    invite = Invite.objects.get(receiver = fullcr,sender = sender_id)
    invite.status = True
    invite.save()
    user = UserProfile.objects.get(id = id)
    user.in_team = True
    user.save()
    return redirect('team')

def reject(request ,id ,cr, sender_id):
    fullcr= "CR"+str(cr)
    
    invite = Invite.objects.get(receiver = fullcr,sender = sender_id)
    invite.decline = True
    invite.save()
    # user = UserProfile.objects.get(id = id)
    # user.in_team = True
    # user.save()
    return redirect('team')

def sendagain(request, id , cr, sender_id):
    # fullcr= "CR"+str(cr)
    invite = Invite.objects.get(receiver = cr,sender = sender_id)
    invite.decline = False
    invite.save()
    return redirect('team')

def newinvite(request):
    if request.method == 'POST':
        name = request.POST['name']
        crid = request.POST['crid']
        current_id = request.POST['current_id']
        sender_id = request.POST['sender_id']
        print(name)
        print(crid)
        print(current_id)
        print(sender_id)
        team ={}
        objs = Team.objects.all()
        for obj in objs:
            if obj.crid2 == current_id:
                obj.member2 = name
                obj.crid2 = crid
                obj.save()

            elif obj.crid3 == current_id:
                obj.member3 = name
                obj.crid3 = crid
                obj.save()

            elif obj.crid4 == current_id:
                obj.member4 = name
                obj.crid4 = crid
                obj.save()

        invite = Invite.objects.get(receiver = current_id,sender = sender_id)
        invite.receiver = crid
        invite.decline = False
        invite.save()
    return redirect('team')

    # else:
    # return HttpResponse("Failed")


    # objes = Invite.objects.all()
    # for obj in objes:
    #     if obj.
    # cr = "CR"+str(cr_id)
    # user = UserProfile.objects.get(id = id)
    # user.in_team = True
    # team.status = True
    # team.save()
    # user.save()
def task(request):
    id =0
    cr_id=0
    obj = UserProfile.objects.get(email= gmail)
    id = obj.id
    cr_id = obj.cr_id
    name = obj.name
    data = { 'name': name , 'crid':cr_id,'id':id}
    return render(request,'user/overall_task.html' ,data)

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


def blog(request):
    id =0
    cr_id=0
    obj = UserProfile.objects.get(email= gmail)
    id = obj.id
    cr_id = obj.cr_id
    name = obj.name
    data = { 'name': name , 'crid':cr_id,'id':id}
    if request.method == "POST":
        bname = request.POST['name']
        crid = request.POST['crid']
        msg = request.POST['message']
        blog = Blog(name = bname, crid= crid, msg = msg)
        blog.save()
        return redirect('blog')

    return render(request, 'user/blog.html' ,data)

def yourprofile(request):
    obj = UserProfile.objects.get(email = gmail)
    data = { 'user': obj }
    return render(request, 'user/inner_profile.html' ,data)


def myprofile(request):
    if request.method == 'POST':
        crid = request.POST['crid']
        name = request.POST['name']
        phone = request.POST['phone']
        whatsapp = request.POST['whatsapp']
        state = request.POST['state']
        year = request.POST['year']
        college = request.POST['college']
        city = request.POST['city']

        user = UserProfile.objects.get(cr_id = crid)
        user.name = name
        user.phone = phone
        user.whatsapp = whatsapp
        user.state = state
        user.year = year
        user.college = college
        user.city = city
        user.save()
    return redirect('yourprofile')    