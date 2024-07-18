from django.contrib import admin
from .models import Gender, Patient, PadreCita, MadreCita, Alergia, InfoMom, Cie10
# Register your models here.

admin.site.register(Gender)
admin.site.register(Patient)
admin.site.register(PadreCita)
admin.site.register(MadreCita)
admin.site.register(Alergia)
admin.site.register(InfoMom)
admin.site.register(Cie10)
