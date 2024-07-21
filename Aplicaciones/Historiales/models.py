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
    ruc_mom=models.CharField(null=True, blank=True, max_length=13)
    dir_mom=models.TextField(null=True,blank=True)
    telf_mom=models.CharField(max_length=10,null=True,blank=True)

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
    ruc_fat=models.CharField(null=True, blank=True, max_length=13)
    dir_fat=models.TextField(null=True,blank=True)
    telf_fat=models.CharField(max_length=10,null=True,blank=True)

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

class Alergia(models.Model):
    id=models.AutoField(primary_key=True)
    creation=models.DateField(default=datetime.date.today)
    nombreAlergia=models.CharField(max_length=150, unique=True)
    def __str__(self):
        return f"{self.id}. {self.nombreAlergia}"


class PatAler(models.Model):
    id = models.AutoField(primary_key=True)
    creation=models.DateField(default=datetime.date.today)
    alergia=models.ForeignKey(Alergia, on_delete=models.CASCADE)
    paciente=models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.paciente} -> {self.alergia}"

class InfoMom(models.Model):
    id = models.AutoField(primary_key=True)
    creation=models.DateField(default=datetime.date.today)
    prenatal=models.TextField()
    natal=models.TextField()
    app=models.TextField()
    apf=models.TextField()
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id} -> Observación de: {self.patient}"

class observaciones(models.Model):
    id = models.AutoField(primary_key=True)
    creation=models.DateField(default=datetime.date.today)
    new_age=models.CharField(max_length=250)
    firstsect= models.TextField()
    secondsect=models.TextField()
    cortesia=models.BooleanField(default=False)
    paciente = models.ForeignKey(Patient,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id} ->Observación de: {self.paciente}"


class Cie10(models.Model):
    id = models.AutoField(primary_key=True)
    cod3 = models.CharField(max_length=10)
    nombrecie=models.CharField(max_length=250)
    def __str__(self):
        return f"{self.cod3}. {self.nombrecie}"

class medicina(models.Model):
    id = models.AutoField(primary_key=True)
    nombregen_med=models.CharField(max_length=150)
    nombrecom_med=models.CharField(max_length=150)
    tipo_med= models.CharField(max_length=150)
    def __str__(self):
        return f"{self.nombrecom_med} -> {self.tipo_med}"
