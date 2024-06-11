from django.contrib import admin
from .models import DiaHorario, HorasDia, UsuarioCli, MadreCita, PadreCita, ContactCita, CitaSol, FactCitas
# Register your models here.

admin.site.register(DiaHorario)
admin.site.register(HorasDia)
admin.site.register(UsuarioCli)
admin.site.register(MadreCita)
admin.site.register(PadreCita)
admin.site.register(ContactCita)
admin.site.register(CitaSol)
admin.site.register(FactCitas)
