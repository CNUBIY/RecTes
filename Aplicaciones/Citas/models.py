from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class GenerosCli (models.Model):
    id=models.AutoField(primary_key=True)
    nombre_gen=models.CharField(max_length=150)

    def __str__(self):
        return f"- {self.nombre_gen}"


class MadreCita(models.Model):
    id= models.AutoField(primary_key=True)
    nom_mom=models.CharField(max_length=150)
    ape_mom=models.CharField(max_length=150)
    age_mom=models.DateField()
    hij_mom=models.IntegerField()
    es_cimom=models.CharField(max_length=150)
    act_mom=models.CharField(max_length=150)
    correo_mom=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nom_mom} {self.ape_mom}"

class PadreCita(models.Model):
    id= models.AutoField(primary_key=True)
    nom_fat=models.CharField(max_length=150)
    ape_fat=models.CharField(max_length=150)
    age_fat=models.DateField()
    act_fat=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nom_fat} {self.ape_fat}"

class ContactCita (models.Model):
    id=models.AutoField(primary_key=True)
    tf_casa=models.CharField(max_length=150)
    cell=models.CharField(max_length=150)
    tf_tra=models.CharField(max_length=150)


class CitaSol(models.Model):
    id=models.AutoField(primary_key=True)
    fech_da=models.DateField()
    time_da=models.TimeField()

    def __str__(self):
        return f"{self.fech_da}-{self.time_da}"





class UsuarioCli(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_us = models.CharField(max_length=150)
    apellido_us = models.CharField(max_length=150)
    correo_us = models.CharField(max_length=150)
    telf_us = models.CharField(null=True, blank=True, max_length=10)
    pass_us = models.CharField(max_length=300)
    gen_us = models.ForeignKey(GenerosCli, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.apellido_us} {self.nombre_us} - {self.correo_us}"


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
