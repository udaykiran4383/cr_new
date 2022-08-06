from unicodedata import name
from django.db import models
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    cr_id = models.CharField(max_length=200, default="")
    name = models.CharField(max_length=200, default="")
    email = models.CharField(max_length=200, default="")
    phone = models.CharField(max_length=200,default="")
    whatsapp = models.CharField(max_length=200,default="")
    state = models.CharField(max_length=200,default="")
    year = models.CharField(max_length=200,default="")
    college = models.CharField(max_length=200,default="")
    city = models.CharField(max_length=200,default="")
    sop = models.CharField(max_length=2000,default="")
    points = models.IntegerField(default="0")
    in_team = models.BooleanField(default='False')
    ref = models.CharField(max_length=200, default="")
    bonus_ref = models.CharField(max_length=200, default="")   #for form
    def __str__(self):
        return self.name


class Leaderboard(models.Model):
    name = models.CharField(max_length=200)
    points = models.CharField(max_length=200)

    def __str__(self):
        return self.name 

class Invite(models.Model):
    sender_name = models.CharField(max_length=200,default="")
    sender = models.CharField(max_length=200)
    sender_cr_id = models.CharField(max_length=200 ,default="")
    receiver = models.CharField(max_length=200)
    status = models.BooleanField(default='False')
    decline = models.BooleanField(default='False')
    
    def __str__(self):
        return self.sender_name 

class Team(models.Model):
    teamname = models.CharField(max_length=200 ,default="")
    leader = models.CharField(max_length=200 ,default="")
    crid1 = models.CharField(max_length=200 ,default="")
    member2 = models.CharField(max_length=200 ,default="")
    crid2 = models.CharField(max_length=200 ,default="")
    member3 = models.CharField(max_length=200 ,default="")
    crid3 = models.CharField(max_length=200 ,default="")
    member4 = models.CharField(max_length=200 ,default="")
    crid4 = models.CharField(max_length=200  ,default="")
    teampoint = models.IntegerField(default="0")
    team_status = models.BooleanField(default='False')
    proof = models.CharField(max_length=1000,default="")
    task1_status = models.BooleanField(default='False')


    def __str__(self):
        return self.teamname 

class Blog(models.Model):
    name = models.CharField(max_length=200)
    crid = models.CharField(max_length=200)
    msg = models.CharField(max_length=5000)