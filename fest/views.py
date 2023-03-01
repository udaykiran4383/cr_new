from django.shortcuts import render
from .serializers import *
from .models import GoogleUser , NormalUser, Event, ConvoUser
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.serializers import serialize
import json

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
            return Response({"name": user.name,"Ano":user.Ano,
        "email": user.email,
        "sdw": user.sdw,
        "csr": user.csr,
        "sebi": user.sebi,
        "cyber": user.cyber,
        "health": user.health,
        "sociotech": user.sociotech,
        "coc": user.coc,
        "menstrual": user.menstrual,
        "csrc": user.csrc,
        "sspe": user.sspe,
        "rap": user.rap,
        "Media": user.Media,
        "eq": user.eq,
        "theatre": user.theatre,
        "manual": user.manual,
        "disable": user.disable,
        "samwaad": user.samwaad,
        "cpr": user.cpr,
        "leader": user.leader,"mental":user.mental,"status":200}) 
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


            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def Event_list(request):
    if request.method == 'GET':
        data = Event.objects.all()

        serializer = EventSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()


            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Event_reg(request):
    if NormalUser.objects.filter(email = request.data["email"]).exists():
       event = request.data["tag"]
       NormalUser.objects.filter(email = request.data["email"]).update(**{event:True})
       return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def ConvoUser_list(request):
    if request.method == 'GET':
        data = ConvoUser.objects.all()

        serializer = ConvoSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ConvoSerializer(data=request.data)
        if ConvoUser.objects.filter(email = request.data["email"]).exists():
            user = ConvoUser.objects.get(email = request.data["email"])
            return Response({"name": user.name,"Ano":user.Ano,
        "email": user.email,
        "status":200}) 
        elif serializer.is_valid():
            serializer.save()


            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
