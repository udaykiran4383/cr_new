from .resources import D2cResource
from tablib import Dataset
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Student ,Team, Mentor, Playbook, D2c
from .serializers import *
import random
import array
# from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import smtplib , ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def password():
    MAX_LEN = 12
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
            '*', '(', ')', '<']
    
    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    
    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)
    
    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    
    
    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
    
        # convert temporary password into array and shuffle to
        # prevent it from having a consistent pattern
        # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    
    # traverse the temporary password array and append the chars
    # to form the password
    password = ""
    for x in temp_pass_list:
            password = password + x
            
    # returns password
    return password

def allmail(email, username , password):
    sender_email = "chirag.abhyuday@gmail.com"  # Enter your address
    receiver_email = email # Enter receiver address
    pas = "qmccznzowjpvicct"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Action Plan 2022"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
Greeting from Abhyuday, IIT Bombay!\n
Welcome to Action Plan 2022, Asia's largest growing Social Entrepreneurship competition.\n
Below are your login credentials:
Username: """ + username + """ 
Password: """ + password + """\n
Further details about workshops and playbook submission will be communicated to you. Stay updated at our website : abhyudayiitb.org/actionplan \n
Thanks and regards,
Team Abhyuday, IIT Bombay 
Email: actionplan.abhyudayiitb@gmail.com
"""
    # html = """\
    # <html>
    # <body>
    #     <a href="http://localhost/aptest/login">Click here</a> 
    #     to Log in
    # </body>
    # </html>
    # """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    # message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, pas)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    print("done")
    

@api_view(['GET', 'POST'])
def students_list(request):
    if request.method == 'GET':
        data = Student.objects.all()

        serializer = StudentSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()



            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def teams_list(request):
    if request.method == 'GET':
        data = Team.objects.all()

        serializer = TeamSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logpass = password()
            name = request.data['teamname']
            try:
                user = User.objects.get(username = name)
                return Response({'error':'The Teamname already exists! Please Try another Teamname'})
            except:
                user = User.objects.create_user(request.data['teamname'], request.data['email1'], logpass)
                email1 = request.data['email1']
                # email2 = request.data['email2']
                # email3 = request.data['email3']
                # email4 = request.data['email4']
                # rece_list = [email1,email2,email3,email4]
                # print(rece_list)
                allmail(email1, name,logpass)
                # allmail(email2, name,logpass)
                # allmail(email3, name,logpass)
                # allmail(email4, name,logpass)
                

                user.save()
                return Response(status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def login_view(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password = password)
    if user is not None:
        auth_login(request, user)
        data = Team.objects.filter(teamname = username)
        serializer = TeamSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET', 'POST'])
def mentors_list(request):
    if request.method == 'GET':
        data = Mentor.objects.all()

        serializer = MentorSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MentorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()



            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def playbooks_list(request):
    if request.method == 'GET':
        data = Playbook.objects.all()

        serializer = PlaybookSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PlaybookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()



            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def simple_upload(request):
    if request.method == 'POST':
        person_resource = D2cResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read(),format='xlsx')
        print(imported_data)
#        for data in imported_data:
#                print(data[1])
#                value = D2c(
#                        data[1],
#                        data[2],
#                         data[3],data[4],
#                        data[5],data[6],
#                         data[7],data[8],
#                         data[9],data[10],
#                        )
#                value.save()       


    return render(request, 'user/input.html')
