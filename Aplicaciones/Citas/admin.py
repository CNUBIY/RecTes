from django.contrib import admin
from .models import CitaDia,NombreDia, DiaHorario, HorasDia
# Register your models here.
admin.site.register(CitaDia)
admin.site.register(NombreDia)
admin.site.register(DiaHorario)
admin.site.register(HorasDia)
