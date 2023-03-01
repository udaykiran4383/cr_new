from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField("Name", max_length=240)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Team(models.Model):
    teamname = models.CharField("Name", max_length=240)
    phone = models.CharField(max_length=200,default="")
    member1 = models.CharField("Name", max_length=240 , default="")
    email1 = models.EmailField(default="")
    member2 = models.CharField("Name", max_length=240 , default="",blank= True)
    email2 = models.EmailField(default="",blank= True)
    member3 = models.CharField("Name", max_length=240 , default="",blank= True)
    email3 = models.EmailField(default="",blank= True)
    member4 = models.CharField("Name", max_length=240 , default="",blank= True)
    email4 = models.EmailField(default="",blank= True)


    def __str__(self):
        return self.teamname

class D2c(models.Model):
    teamname = models.CharField("Name", max_length=240)
    phone = models.CharField(max_length=200,default="")
    member1 = models.CharField("Name", max_length=240 , default="")
    email1 = models.EmailField(default="")
    member2 = models.CharField("Name", max_length=240 , default="",blank= True)
    email2 = models.EmailField(default="",blank= True)
    member3 = models.CharField("Name", max_length=240 , default="",blank= True)
    email3 = models.EmailField(default="",blank= True)
    member4 = models.CharField("Name", max_length=240 , default="",blank= True)
    email4 = models.EmailField(default="",blank= True)


    def __str__(self):
        return self.teamname


class Mentor(models.Model):
    name = models.CharField("Name", max_length=240)
    email = models.EmailField(default="")
    contact = models.CharField("Contact", max_length=240 , default="")
    firm = models.CharField("Firm", max_length=240 , default="", )
    desig = models.CharField("Designation", max_length=240 , default="",)

    def __str__(self):
        return self.name

class Playbook(models.Model):
    teamname = models.CharField("Name", max_length=240)
    sector = models.CharField("Sector", max_length=240)
    q1 = models.CharField("What problem is your team trying to solve and what solution do you propose? ", max_length=5000 , default="")
    q2 = models.CharField("Who are the major stakeholders (key partners) in your startup? ", max_length=5000 , default="", )
    q3 = models.CharField("Who are your major customer segments? ", max_length=5000 , default="",)
    q4 = models.CharField("Describe your market share through TAM, SAM, SOM.  ", max_length=5000 , default="",)
    q5 = models.CharField("What is a unique value proposition that your startup builds upon?  ", max_length=5000 , default="",)
    q6 = models.CharField("What is your business model for your startup? How are you generating revenue?  ", max_length=5000 , default="",)
    q7 = models.CharField("Are there any competitors working on the same project?  If yes , mention how you are better than them.", max_length=5000 , default="",)
    q8 = models.CharField("Are you full time working on your startup or partial?  ", max_length=5000 , default="",)

    def __str__(self):
        return self.teamname
