from django.db import models

# Create your models here.
class GoogleUser(models.Model):
    name = models.CharField("Name",max_length=240)
    email = models.EmailField()

    def __str__(self) :
        return self.name

class NormalUser(models.Model):
    Ano = models.CharField("Ticket No.", max_length=240 , default="")
    name = models.CharField("Name", max_length=240)
    email = models.EmailField(default="")
    contact = models.CharField("Contact", max_length=240 , default="")
    sdw = models.BooleanField("Self Defence",default=False)
    csr = models.BooleanField("CSR",default=False)
    sebi = models.BooleanField("SEBI",default=False)
    cyber = models.BooleanField("Cyber",default=False)
    health = models.BooleanField("Health Checkup",default=False)
    sociotech = models.BooleanField("Socio Tech",default=False)
    coc = models.BooleanField("Concert",default=False)
    menstrual = models.BooleanField("Menstrual",default=False)
    csrc = models.BooleanField("CSR Conclave",default=False)
    sspe = models.BooleanField("Small Scale",default=False)
    rap = models.BooleanField("Rap Battle",default=False)
    Media = models.BooleanField("Media Conclave",default=False)
    eq = models.BooleanField("EQ",default=False)
    theatre = models.BooleanField("Theatre Play",default=False)
    manual = models.BooleanField("MANUAL Scavanging",default=False)
    disable = models.BooleanField("Disability",default=False)
    samwaad = models.BooleanField("Samwaad",default=False)
    cpr = models.BooleanField("CPR Workshop",default=False)
    leader = models.BooleanField("Leadership Program",default=False)
    block = models.BooleanField("Blockchain Sustainibility",default=False)
    mental = models.BooleanField("Ananya Birla",default=False)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField("Name", max_length=240)
    imgurl = models.CharField("Image Url", max_length=1000)
    type = models.CharField("Type", max_length=240)
    tag = models.CharField("Tag", max_length=240,default="")
    def __str__(self):
        return self.name

class ConvoUser(models.Model):
    Ano = models.CharField("Ticket No.", max_length=240 , default="")
    name = models.CharField("Name", max_length=240)
    email = models.EmailField(default="")
    contact = models.CharField("Contact", max_length=240 , default="")

    def __str__(self):
        return self.name
