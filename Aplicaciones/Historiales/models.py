from django.db import models

# Create your models here.
class Patient(models.Model):
    idPat=models.AutoField(primary_key=True)
    lastnPat=models.CharField(max_length=150)
    namePat=models.CharField(max_length=150)
    pldatePat=models.TextField()
    birthPat=models.DateField()
    fagePat=models.CharField(max_length=150)
    natiPat=models.CharField(max_length=150)
    placePat=models.TextField(max_length=150)
    ciPat=models.CharField(max_length=10)
