from rest_framework import serializers
from .models import NormalUser, GoogleUser

class GoogleSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoogleUser 
        fields = ('pk', 'name', 'email')


class NormalSerializer(serializers.ModelSerializer):

    class Meta:
        model = NormalUser 
        fields = ('pk', 'name',  'email', 'contact', 'school' ,'age')
