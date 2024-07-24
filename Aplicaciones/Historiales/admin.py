from django.contrib import admin
from .models import Gender, Patient, PadreCita, MadreCita, Alergia, InfoMom, Cie10, medicina, Diagnostico, Receta
# Register your models here.

admin.site.register(Gender)
admin.site.register(Patient)
admin.site.register(PadreCita)
admin.site.register(MadreCita)
admin.site.register(Alergia)
admin.site.register(InfoMom)
admin.site.register(Cie10)
admin.site.register(medicina)
admin.site.register(Diagnostico)
admin.site.register(Receta)
