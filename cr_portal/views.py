from .resources import TeamResource
from tablib import Dataset
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
import pandas as pd

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



def dashboard(request , id):
    main = User.objects.get(id = id)
    email = main.email
    try:
        user = UserProfile.objects.get(email=email)
        data={'id':id, 'my':user}
        return render(request, 'user/dashboard.html',data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id,'email':email}
        return render(request, 'user/profile.html',data)

            

def updateprofile(request, id ):
    if request.method == 'POST':
        li=range(1000,5000)
        cr_global = random.sample(li,1)
        referral = random.sample(li,1)
        # MH xx AE xxxx
        # CR 23 MH 1234
        ref="REF"+ str(referral[0])
        myid = request.POST['myid']
        name = request.POST['name']
        email = request.POST['email']
        ref = ref
        phone = request.POST['phone']
        whatsapp = request.POST['whatsapp']
        state = request.POST['state']
        state_code = ""
        if (state == 'Delhi'):
            state_code = "DL"
        elif (state == 'Maharashtra'):
            state_code = "MH"
        elif (state == 'Uttar Pradesh'):
            state_code = "UP"
        elif (state == 'Madhya Pradesh'):
            state_code = "MP"
        elif (state == 'Arunachal Pradesh'):
            state_code = "AR"
        elif( state == 'Andaman and Nicobar Islands'):
            state_code = "AN"
        elif (state == 'Assam'):
            state_code = "AS"
        elif( state == 'Bihar'):
            state_code = "BH"
        elif (state == 'Chandigarh'):
            state_code = "CH"
        elif (state == 'Dadar and Nagar Haveli'):
            state_code = "DN"
        elif (state == 'Chhattisgarh'):
            state_code = "CT"
        elif (state == 'Daman and Diu'):
            state_code = "DD"
        elif (state == 'Lakshadweep'):
            state_code = "LD"
        elif (state == 'Puducherry'):
            state_code = "PC"
        elif (state == 'Goa'):
            state_code = "GO"
        elif (state == 'Gujarat'):
            state_code = "GJ"
        elif (state == 'Haryana'):
            state_code = "HR"
        elif (state == 'Himachal Pradesh'):
            state_code = "HP"
        elif (state == 'Jammu and Kashmir'):
            state_code = "JK"
        elif (state == 'Jharkhand'):
            state_code = "JK"
        elif (state == 'Karnataka'):
            state_code = "KT"
        elif (state == 'Kerala'):
            state_code = "KR"
        elif (state == 'Manipur'):
            state_code = "MN"
        elif (state == 'Meghalaya'):
            state_code = "MG"
        elif (state == 'Mizoram'):
            state_code = "MZ"
        elif (state == 'Nagaland'):
            state_code = "NG"
        elif (state == 'Odisha'):
            state_code = "OD"
        elif (state == 'Punjab'):
            state_code = "PJ"
        elif (state == 'Rajasthan'):
            state_code = "RJ"
        elif (state == 'Sikkim'):
            state_code = "SK"
        elif (state == 'Tamil Nadu'):
            state_code = "TN"
        elif (state == 'Telangana'):
            state_code = "TL"
        elif (state == 'Tripura'):
            state_code = "TR"
        elif (state == 'Uttarakhand'):
            state_code = "UK"
        else:
            state_code = "WB"                                                                     
        cr=  "CR 23 " + state_code + " " + str(cr_global[0])
        year = request.POST['year']
        college = request.POST['college']
        city = request.POST['city']
        sop = request.POST['sop']
        cr_id = cr
        bonus = request.POST['bonus']
        info = UserProfile(cr_id=cr_id,name= name,email=email,phone=phone, whatsapp = whatsapp, state=state, year=year,college=college,city=city,sop=sop,ref=ref,bonus_ref=bonus)
        info.save()
        sub = "Congratulations for enrolling in CR Program of Abhyuday IIT Bombay"
        msg = """Congratulations """ + name+"""!! \n
You have successfully registered in the College Representative Internship Program 2022-23 of Abhyuday, IIT Bombay! We welcome you to the Abhyuday family! \n
Your College Representative ID for your tenure as a CR will be """ +str(cr)+""". \n
You would soon receive your Coding Ninjas discount coupons! \n
You can share the following referral code with your friends from your college to form a team and with other friends to earn more points for your team. \nReferral Code - """ +str(ref)+ """\n
Lots of good wishes for your new endeavours with Abhyuday, IIT Bombay. \n"Do what you can, with what you have, where you are." -Theodore Roosevelt \n
Regards, \nAbhyuday"""
        send_mail(
                sub, msg, 'cr.abhyuday.iitbombay@gmail.com',[email]
            )
        return redirect('dashboard', id = myid)

def leaderboard(request , id):
    main = User.objects.get(id = id)
    email = main.email
    try:
        user = UserProfile.objects.get(email=email)
        team = Team.objects.filter(team_status = True).order_by('-teampoint')
        myid = user.id
        cr_id = user.cr_id
        mypoint = user.points
        inteam = user.in_team

        data1 = UserProfile.objects.filter( in_team = False ).order_by('-points')

        myrank =0
        for idx, obj in enumerate(data1):
            if obj.cr_id == cr_id:
                myrank = idx + 1

        team_rank =0
        for idy, obj in enumerate(team):
            if (obj.crid1 == cr_id) or (obj.crid2 == cr_id) or (obj.crid3 == cr_id) or (obj.crid4 == cr_id):
                team_rank = idy + 1
    
        team_point =0
        objs = Team.objects.all()
        for obj in objs:
            if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
                team_point = obj.teampoint

        data={'id':id, 'my':user,"user": data1,'myid':myid,'cr_id':cr_id,'teams':team,'rank':myrank , 'teamrank':team_rank, 'teampoint':team_point , 'mypoint':mypoint , 'inteam':inteam}
        return render(request, 'user/leaderboard.html',data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)



def team(request ,id):
    main = User.objects.get(id = id)
    email = main.email
    try:
        user = UserProfile.objects.get(email=email)
        team = Team.objects.filter(team_status = True)
        name = user.name
        cr_id = user.cr_id
        inteam = user.in_team
        if request.method == "POST":
            teamname = request.POST['teamname']
            leader = request.POST['teamleader']
            cr_id1 = request.POST['crid1']
            member2 = request.POST['member2']
            cr_id2 = request.POST['crid2']
            # print("CR ID: ",cr_id2)
            # print("LENGTH OF CR ID: ",len(cr_id2))
            # if(len(cr_id2) < 12):
            #     return render(request, 'index.html')
            member3 = request.POST['member3']
            cr_id3 = request.POST['crid3']
            member4 = request.POST['member4']
            cr_id4 = request.POST['crid4']
            team = Team(teamname = teamname, leader=leader,crid1 = cr_id1,member2 = member2,crid2=cr_id2,member3=member3, crid3 = cr_id3,member4=member4,crid4=cr_id4)
            objes = UserProfile.objects.all()
            member = UserProfile.objects.get(email =email)
            member.in_team = True
            member.is_individual = False
            member.save()
            invite2 = Invite(sender_name = leader, sender= id, sender_cr_id = cr_id , receiver = cr_id2)
            invite2.save()
            invite3 = Invite(sender_name = leader, sender= id, sender_cr_id = cr_id ,receiver = cr_id3)
            invite3.save()   
            if member4 != "":
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

        cr= ""
        for m in cr_id:
            if m.isdigit():
                cr = cr + m
    
        numcr = int(cr)
        if team !=0:
            teamreg = Invite.objects.filter(sender_cr_id = team.crid1)
#            count = 0
#            for obj in teamreg:
#               if obj.status == True:
#                    count= count +1

#                if count == 3 or count == 2:
#                    team.team_status = True
#                    team.save()
#                else:
#                    team.team_status = False
#                    team.save() 
            data ={
                'teamreg':teamreg,
                'name':name,'cr_id':cr_id,'id':id,
                'team':team,'teamname':team.teamname,'leader':team.leader,'team_status':team.team_status,'leader_id':team.crid1,'cr':numcr , 'temp':temp ,'inteam':inteam, 'user': user
            }
            return render(request , 'user/team.html',data )
        else:
            data ={
                'name':name,'cr_id':cr_id,'id':id,'temp':temp ,'inteam':inteam
            }
            return render(request , 'user/team.html',data )

    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)


def invite(request , id):
    main = User.objects.get(id = id)
    email = main.email
    try:
        user1 = UserProfile.objects.get(email=email)
        name = user1.name
        cr_id = user1.cr_id
        invite_data = Invite.objects.filter(receiver = cr_id)
        cr= ""
        for m in cr_id:
            if m.isdigit():
                cr = cr + m
    
        numcr = int(cr)
        data={'id':id, 'my':user1,"invite": invite_data,"name":name,'cr':numcr,'cr_id':cr_id}
        return render(request, 'user/invite.html',data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)

def accept(request ,id ,cr, sender_id):
    main = User.objects.get(id = id)
    email = main.email
    try:
       invite = Invite.objects.get(receiver = cr, sender_cr_id = sender_id)
       invite.status = True
       invite.save()
       user = UserProfile.objects.get(email=email)
       user.in_team = True
       user.save()
       data={'id':id, 'my':user}
       return redirect('team', id = id)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)

def reject(request ,id ,cr, sender_id):
    main = User.objects.get(id = id)
    email = main.email
    try:
       invite = Invite.objects.get(receiver = cr, sender_cr_id = sender_id)
       invite.decline = True
       invite.save()
       user = UserProfile.objects.get(email=email)
       user.in_team = False
       user.save()
       data={'id':id, 'my':user}
       return redirect('team', id = id)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)

def sendagain(request, id , cr, sender_id):
    main = User.objects.get(id = id)
    email = main.email
    try:
       invite = Invite.objects.get(receiver = cr, sender_cr_id = sender_id)
       invite.decline = False
       invite.save()
       data={'id':id}
       return redirect('team', id = id)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)

def newinvite(request , id):
    main = User.objects.get(id = id)
    email = main.email
    try:
       if request.method == 'POST':
           name = request.POST['name']
           crid = request.POST['crid']
           current_id = request.POST['current_id']
           sender_id = request.POST['sender_id']
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

       return redirect('team', id = id)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)

def task(request , id):
    main = User.objects.get(id = id)
    email = main.email
    try:
        user = UserProfile.objects.get(email=email)
        data={'id':id, 'my':user}
        return render(request, 'user/overall_task.html',data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)

def task1(request ,id):
    main = User.objects.get(id = id)
    email = main.email
    try:
       user = UserProfile.objects.get(email=email)
       cr_id = user.cr_id

       if request.method == "POST":
           proof = request.POST['proof']
           if user.in_team == True:
               team ={}
               objs = Team.objects.all()
               for obj in objs:
                  if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
                    team = obj
               if team.team_status == True:
                      team.proof = proof
                      team.task1_status = False
                      team.save()
               data={'id':id,'cr_id':cr_id,'inteam':user.in_team,'teamform':team.team_status,'task':team.task1_status}
               return render(request, 'user/task1.html',data)
           elif user.in_team == False:
               user.proof = proof
               user.task1_status = False
               user.save()
               data={'id':id,'cr_id':cr_id,'inteam':user.in_team,'task':user.task1_status}
               return render(request, 'user/task1.html',data)
           else:
              return redirect('team' , id=id)
       data={'id':id,'cr_id':cr_id,'inteam':user.in_team,'task':user.task1_status}
       return render(request, 'user/task1.html',data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)
    
def task2(request ,id):
    main = User.objects.get(id = id)
    email = main.email
    try:
       user = UserProfile.objects.get(email=email)
       cr_id = user.cr_id

       if request.method == "POST":
           proof = request.POST['proof2']
           if user.in_team == True:
               team ={}
               objs = Team.objects.all()
               for obj in objs:
                  if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
                    team = obj
               if team.team_status == True:
                      team.proof2 = proof
                      team.task2_status = False
                      team.save()
               data={'id':id,'cr_id':cr_id,'inteam':user.in_team,'teamform':team.team_status,'task2':team.task2_status}
               return render(request, 'user/task2.html',data)
           elif user.in_team == False:
               user.proof2 = proof
               user.task2_status = False
               user.save()
               data={'id':id,'cr_id':cr_id,'inteam':user.in_team,'task2':user.task2_status}
               return render(request, 'user/task2.html',data)
           else:
              return redirect('team' , id=id)
       data={'id':id,'cr_id':cr_id,'inteam':user.in_team,'task2':user.task2_status}
       return render(request, 'user/task2.html',data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)
    
def task3(request ,id):
    main = User.objects.get(id = id)
    email = main.email
    try:
       user = UserProfile.objects.get(email=email)
       cr_id = user.cr_id

       if request.method == "POST":
           proof = request.POST['proof3']
           if user.in_team == True:
               team ={}
               objs = Team.objects.all()
               for obj in objs:
                  if obj.crid1 == cr_id or obj.crid2 == cr_id or obj.crid3 == cr_id or obj.crid4 == cr_id:
                    team = obj
               if team.team_status == True:
                      team.proof3 = proof
                      team.task3_status = False
                      team.save()
               data={'id':id,'cr_id':cr_id,'inteam':user.in_team,'teamform':team.team_status,'task3':team.task3_status}
               return render(request, 'user/task3.html',data)
           elif user.in_team == False:
               user.proof3 = proof
               user.task3_status = False
               user.save()
               data={'id':id,'cr_id':cr_id,'inteam':user.in_team,'task3':user.task3_status}
               return render(request, 'user/task3.html',data)
           else:
              return redirect('team' , id=id)
       data={'id':id,'cr_id':cr_id,'inteam':user.in_team,'task3':user.task3_status}
       return render(request, 'user/task3.html',data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)


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


def blog(request,id):
    main = User.objects.get(id = id)
    email = main.email
    try:
        user = UserProfile.objects.get(email=email)
        cr_id = user.cr_id
        name = user.name
        data = { 'name': name , 'crid':cr_id,'id':id}
        if request.method == "POST":
            bname = request.POST['name']
            crid = request.POST['crid']
            msg = request.POST['message']
            blog = Blog(name = bname, crid= crid, msg = msg)
            blog.save()
            return redirect('blog', id=id)

        return render(request, 'user/blog.html' ,data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)

def yourprofile(request ,id):
    main = User.objects.get(id = id)
    email = main.email
    try:
        user = UserProfile.objects.get(email=email)
        data={'id':id, 'user':user}
        return render(request, 'user/inner_profile.html',data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)


def myprofile(request ,id):
    main = User.objects.get(id = id)
    email = main.email
    try:
        if request.method == 'POST':
            crid = request.POST['crid']
            name = request.POST['name']
            phone = request.POST['phone']
            whatsapp = request.POST['whatsapp']
            state = request.POST['state']
            year = request.POST['year']
            college = request.POST['college']
            city = request.POST['city']

            user = UserProfile.objects.get(email=email)
            user.name = name
            user.phone = phone
            user.whatsapp = whatsapp
            user.state = state
            user.year = year
            user.college = college
            user.city = city
            user.save()

        data={'id':id, 'user':user}
        return render(request, 'user/inner_profile.html',data)
    except UserProfile.DoesNotExist:
        user = None
        data = {'id':id , 'email':email}
        return render(request, 'user/profile.html' ,data)









def export(request):
    objs = UserProfile.objects.all()
    data =[]

    for obj in objs:
        data.append({
            "Name": obj.name,
            "CR ID":obj.cr_id,
            "Team Name":obj.tname,
            "Email":obj.email,
            "Contact":obj.whatsapp,
            "Referal Count":obj.refer_count,
            "City":obj.city,
            "College":obj.college,
            "In team":obj.in_team,
            "State":obj.state,
        "sop" : obj.sop,
            "Year":obj.year,
            "Proof Submission":obj.proof,
        })

    pd.DataFrame(data).to_excel('output.xlsx')
    return JsonResponse({
        'status':200
    })
def teamexport(request):
    objs = Team.objects.all()
    data =[]

    for obj in objs:
        data.append({
            "Team Name": obj.teamname,
            "Leader":obj.leader,
            "CR ID 1":obj.crid1,
            "Member 2":obj.member2,
            "CR ID 2": obj.crid2,
            "Member 3":obj.member3,
            "CR ID 3":obj.crid3,
            "Member 4":obj.member4,
            "CR ID 4":obj.crid4,
            "Team status":obj.team_status,
            "Proof Submission":obj.proof,
        })

    pd.DataFrame(data).to_excel('teamoutput.xlsx')
    return JsonResponse({
        'status':200
    })

def teamsort(request):
    objs = Team.objects.all()
    objes = UserProfile.objects.all()
    
    for obj in objes:
       for ob in objs:
           if obj.cr_id == ob.crid1 or obj.cr_id == ob.crid2 or obj.cr_id == ob.crid3 or obj.cr_id == ob.crid4:
               obj.tname = ob.teamname
               obj.save()
               break

    return HttpResponse("Done")

def google(request):
    objs = User.objects.all()
    data =[]

    for obj in objs:
        data.append({
            "Name": obj.username,
            "Email":obj.email,
        })

    pd.DataFrame(data).to_excel('google.xlsx')
    return JsonResponse({
        'status':200
    })

def ref_count(request):
   allobj = UserProfile.objects.all()
   for obj in allobj:
      objs = UserProfile.objects.filter(bonus_ref = obj.ref)
      obj.refer_count = objs.count()
      if objs.count() >=15:
         obj.points = 200 + (objs.count() - 15 )*10
      else:
         obj.points = (objs.count())*10
      obj.save()
   
   teamobj = Team.objects.all()
   for ob in teamobj:
      ref = 0
      for obj in allobj:
         if obj.cr_id  == ob.crid1 or obj.cr_id == ob.crid2 or obj.cr_id == ob.crid3 or obj.cr_id == ob.crid4:
             ref = ref + obj.refer_count
      if ref >= 15:
         ob.teampoint = 200 +(ref - 15 )*10
      else:
         ob.teampoint = ref*10
      ob.save()

   return HttpResponse("Done")


def simple_upload(request):
    if request.method == 'POST':
        person_resource = TeamResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read(),format='xlsx')
        #print(imported_data)
        for data in imported_data:
            print(data[1])
            value = Team(
                data[0],
                data[1],
                 data[2],data[3],
                 data[4],data[5],
                         data[6],data[7],
                         data[8],data[9],
                )
            value.save()       
        
        #result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        #if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'user/input.html')

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
                sub, msg, 'cr.abhyuday.iitbombay@gmail.com',[obj.email]
            )

   return HttpResponse("Done")
