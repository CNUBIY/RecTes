from django import forms
from .models import CitaSol

class CitaSolForm(forms.ModelForm):
    class Meta:
        model = CitaSol
        fields = ['fech_da', 'time_da', 'cort_da', 'nom_da', 'est_da']
        widgets = {
            'time_da': forms.TimeInput(format='%H:%M'),  # Formato de 24 horas
        }
