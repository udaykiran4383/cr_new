from django.db import models

# Create your models here.
class GoogleUser(models.Model):
    name = models.CharField("Name",max_length=240)
    email = models.EmailField()

    def __str__(self) :
        return self.name

class NormalUser(models.Model):
    name = models.CharField("Name", max_length=240)
    email = models.EmailField(default="")
    contact = models.CharField("Contact", max_length=240 , default="")
    school = models.CharField("Institute", max_length=240 , default="", )
    age = models.PositiveIntegerField("Age",  default="")

    def __str__(self):
        return self.name
