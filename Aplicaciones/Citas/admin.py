from django.contrib import admin
from .models import DiaHorario, HorasDia, UsuarioCli, GenerosCli
# Register your models here.

admin.site.register(DiaHorario)
admin.site.register(HorasDia)
admin.site.register(UsuarioCli)
admin.site.register(GenerosCli)
