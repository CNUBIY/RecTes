from django.db import models
import datetime
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
    num=models.ForeignKey(ContactCita, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.lastnPat} {self.namePat} - {self.ciPat}"
