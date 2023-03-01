from django.shortcuts import render
from .serializers import *
from .models import GoogleUser , NormalUser
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import smtplib , ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def allmail(email,name):
    sender_email = "services.abhyudayiitb@gmail.com"  # Enter your address
    receiver_email = email # Enter receiver address
    pas = "cetedfalwcvdrofm"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Youth Delegate Program | Abhyuday, IIT Bombay"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
Congratulations """ + name  +"""!!\n
You have successfully registered in the Youth Delegate Program 2023 of Abhyuday, IIT Bombay! We welcome you to the Abhyuday family!\n
We cordially invite you to attend and participate on 21st and 22nd January in the Annual Social Fest of Abhyuday, IIT Bombay.\n
To know more details - check out our Instagram handle and give us a follow there!\n
https://www.instagram.com/iitbombay_abhyuday/  \n
Please join the WhatsApp group to get all the updates - https://chat.whatsapp.com/CveJ5vl0IuZ9epNV9VjF2p  \n
Leadership is the capacity to translate vision into reality. —Warren Bennis \n
Lots of good wishes for your new endeavours with Abhyuday, IIT Bombay.\n
Regards,
Abhyuday
"""

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



@api_view(['GET', 'POST'])
def GoogleUser_list(request):
    if request.method == 'GET':
        data = GoogleUser.objects.all()

        serializer = GoogleSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GoogleSerializer(data=request.data)
        if NormalUser.objects.filter(email = request.data["email"]).exists():
            user = NormalUser.objects.get(email = request.data["email"])
            return Response({"name":user.name,"email":user.email,"school":user.school,"age":user.age,"status":200}) 
        elif serializer.is_valid():
            serializer.save()


            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def NormalUser_list(request):
    if request.method == 'GET':
        data = NormalUser.objects.all()

        serializer = NormalSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NormalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            allmail(request.data["email"],request.data["name"])


            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
