from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import UsuarioCli, GenerosCli

class RegistroForm(forms.ModelForm):
    pass_us = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        validators=[validate_password]
    )
    confpass_us = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput
    )

    class Meta:
        model = UsuarioCli
        fields = ['nombre_us', 'apellido_us', 'correo_us', 'pass_us', 'gen_us']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("pass_us")
        confirm_password = cleaned_data.get("confpass_us")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confpass_us', "Las contraseñas no coinciden")

        return cleaned_data
