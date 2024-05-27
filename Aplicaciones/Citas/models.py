from django.db import models

# Create your models here.

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
