from rest_framework import serializers
from .models import NormalUser, GoogleUser, Event,ConvoUser

class GoogleSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoogleUser 
        fields = ('pk', 'name', 'email')


class NormalSerializer(serializers.ModelSerializer):

    class Meta:
        model = NormalUser 
        fields = ('pk','Ano', 'name',  'email', 'contact','sdw','csr','sebi','cyber','health','sociotech','coc','menstrual','csrc','sspe','rap','Media','eq','theatre','manual','disable','samwaad','cpr','leader','block','mental')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event 
        fields = ('pk', 'name', 'imgurl','type','tag')

class ConvoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConvoUser
        fields = ('pk','Ano', 'name',  'email', 'contact')
