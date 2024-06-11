from django.db import models
import datetime
# Create your models here.
class Gender(models.Model):
    id=models.AutoField(primary_key=True)
    nombreGen=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombreGen}"

class Patient(models.Model):
    idPat=models.AutoField(primary_key=True)
    creation=models.DateField(default=datetime.date.today)
    lastnPat=models.CharField(max_length=150)
    namePat=models.CharField(max_length=150)
    pldatePat=models.TextField()
    birthPat=models.DateField()
    fagePat=models.CharField(max_length=150)
    natiPat=models.CharField(max_length=150)
    placePat=models.TextField(max_length=150)
    ciPat=models.CharField(max_length=10)
    genPat=models.ForeignKey(Gender, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.lastnPat} {self.namePat} - {self.ciPat}"
