from django.db import models

# Create your models here.
class NombreDia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=100)

    def __str__(self):
        fila="{0}"
        return fila.format(self.nombre)

class HorasDia(models.Model):
    id=models.AutoField(primary_key=True)
    horaInicio=models.TimeField()
    horaFinal=models.TimeField()

    def __str__(self):
        return f"{self.horaInicio} - {self.horaFinal}"

class CitaDia (models.Model):
    id = models.AutoField(primary_key=True)
    fechaCita = models.DateField()
    dia = models.ForeignKey(NombreDia,null=True,blank=True, on_delete=models.PROTECT)

    def __str__(self):
        fila="{0}"
        return fila.format(self.fechaCita)

class DiaHorario (models.Model):
    id = models.AutoField(primary_key=True)
    diaH=models.ForeignKey(CitaDia, on_delete=models.PROTECT)
    horario=models.ForeignKey(HorasDia, null=True, blank=True, on_delete=models.PROTECT)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.horario} - Disponible: {self.estado}"
