from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class GenerosCli (models.Model):
    id=models.AutoField(primary_key=True)
    nombre_gen=models.CharField(max_length=150)

    def __str__(self):
        return f"- {self.nombre_gen}"

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
