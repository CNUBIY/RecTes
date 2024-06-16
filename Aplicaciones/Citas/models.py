from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.


class CitaSol(models.Model):
    id=models.AutoField(primary_key=True)
    fech_da=models.DateField()
    time_da=models.TimeField()
    cort_da=models.BooleanField(default=False)
    nom_da=models.CharField(max_length=150)
    telf_da=models.CharField(max_length=10)
    est_da=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom_da}: {self.fech_da} | {self.time_da}"

class FactCitas(models.Model):
    id=models.AutoField(primary_key=True)
    idfac=models.CharField(max_length=150)
    descfac=models.CharField(max_length=150)
    valfac=models.DecimalField(max_digits=5, decimal_places=2)
    obsfac=models.CharField(max_length=150)
    fechfac=models.ForeignKey(CitaSol,null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.idfac}-{self.fechfac}"


class UsuarioCli(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_cli = models.CharField(max_length=150)
    correo_cli = models.CharField(max_length=150)
    pass_cli = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.nombre_cli} - {self.correo_cli}"


class HorasDia(models.Model):
    id=models.AutoField(primary_key=True)
    horaInicio=models.TimeField()
    horaFinal=models.TimeField()

    def __str__(self):
        return f"{self.horaInicio} - {self.horaFinal} -{self.id}"

class DiaHorario (models.Model):
    id = models.AutoField(primary_key=True)
    diaH=models.DateField(null=True, blank=True)
    horario=models.ForeignKey(HorasDia, null=True, blank=True, on_delete=models.PROTECT)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.horario} - Disponible: {self.estado} - {self.id} - {self.diaH}"
