from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password
import datetime
from datetime import date

# Create your models here.


class CitaSol(models.Model):
    id=models.AutoField(primary_key=True)
    creation = models.DateField(default=datetime.date.today)
    fech_da=models.DateField()
    time_da=models.TimeField()
    cort_da=models.BooleanField(default=False)
    nom_da=models.CharField(max_length=150)
    telf_da=models.CharField(max_length=10)
    correo_da=models.CharField(null=True, blank=True, max_length=250)
    est_da=models.BooleanField(default=False)
    notificacion_enviada = models.BooleanField(default=False)

    def __str__(self):
        time_formatted = self.time_da.strftime("%I:%M %p")  # Formato de 12 horas con AM/PM sin segundos
        return f"{self.nom_da}: {self.fech_da} a las {time_formatted} por favor comunicarse a {self.telf_da}"

class FactCitas(models.Model):
    id=models.AutoField(primary_key=True)
    creation = models.DateField(default=datetime.date.today)
    idfac=models.CharField(max_length=150)
    descfac=models.CharField(max_length=150)
    valfac=models.DecimalField(max_digits=5, decimal_places=2)
    obsfac=models.CharField(max_length=150)
    fechfac=models.ForeignKey(CitaSol,null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.idfac}-{self.fechfac}"

class SolCli(models.Model):
    idCi = models.AutoField(primary_key=True)
    creation = models.DateField(default=datetime.date.today)
    nom_da=models.CharField(max_length=150)
    telf_da=models.CharField(max_length=10)
    correo_da=models.CharField(null=True, blank=True, max_length=250)
    comentario=models.TextField(null=True,blank=True)
    def __str__(self):
        return f"{self.creation}-{self.nom_da}"
