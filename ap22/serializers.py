
from rest_framework import serializers
from .models import Student, Team, Mentor, Playbook, D2c

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student 
        fields = ('pk', 'name', 'email')


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team 
        fields = ('pk', 'teamname','phone', 'member1', 'email1', 'member2','email2', 'member3' ,'email3', 'member4', 'email4')

class D2cSerializer(serializers.ModelSerializer):

    class Meta:
        model = D2c 
        fields = ('pk', 'teamname','phone', 'member1', 'email1', 'member2','email2', 'member3' ,'email3', 'member4', 'email4')


class MentorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentor 
        fields = ('pk', 'name',  'email', 'contact', 'firm' ,'desig')

class PlaybookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playbook 
        fields = ('pk', 'teamname',  'sector', 'q1', 'q2' ,'q3','q4','q5','q6','q7','q8')
