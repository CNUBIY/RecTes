from django.db import models

# Create your models here.
class Patient(models.Model):
    idPat=models.AutoField(primary_key=True)
    
