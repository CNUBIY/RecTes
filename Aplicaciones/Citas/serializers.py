from rest_framework import serializers
from .models import DiaHorario

class DiaHorarioSerializer(serializers.ModelSerializer):
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = DiaHorario
        fields = ['start', 'end', 'title']

    def get_start(self, obj):
        return f"{obj.diaH}T{obj.horario.horaInicio}"

    def get_end(self, obj):
        return f"{obj.diaH}T{obj.horario.horaFinal}"

    def get_title(self, obj):
        estado = 'Ocupado' if obj.estado else 'Disponible'
        return f"{estado}\r\n{obj.horario.horaInicio} - {obj.horario.horaFinal}"
