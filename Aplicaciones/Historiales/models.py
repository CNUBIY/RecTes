from django.db import models
import datetime
from datetime import date
# Create your models here.
class Gender(models.Model):
    id=models.AutoField(primary_key=True)
    nombreGen=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombreGen}"

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
    @property
    def edad_mom(self):
        today = date.today()
        return today.year - self.age_mom.year - ((today.month, today.day) < (self.age_mom.month, self.age_mom.day))

class PadreCita(models.Model):
    id= models.AutoField(primary_key=True)
    nom_fat=models.CharField(max_length=150)
    ape_fat=models.CharField(max_length=150)
    age_fat=models.DateField()
    act_fat=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nom_fat} {self.ape_fat}"
    @property
    def edad_dad(self):
        today = date.today()
        return today.year - self.age_fat.year - ((today.month, today.day) < (self.age_fat.month, self.age_fat.day))


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
    mom=models.ForeignKey(MadreCita, null=True, blank=True, on_delete=models.PROTECT)
    dad=models.ForeignKey(PadreCita, null=True, blank=True, on_delete=models.PROTECT)
    tf_casa=models.CharField(null=True, blank=True, max_length=10)
    cell=models.CharField(null=True, blank=True, max_length=10)
    tf_tra=models.CharField(null=True, blank=True, max_length=10)
    seguroPat=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lastnPat} {self.namePat} - {self.ciPat}"
