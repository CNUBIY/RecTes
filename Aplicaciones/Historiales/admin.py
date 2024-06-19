from django.contrib import admin
from .models import Gender, Patient, PadreCita, MadreCita
# Register your models here.

admin.site.register(Gender)
admin.site.register(Patient)
admin.site.register(PadreCita)
admin.site.register(MadreCita)
