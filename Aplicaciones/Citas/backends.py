from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import UsuarioCli

class EmailBackend(BaseBackend):
    def authenticate(self, request, correo_us=None, password=None):
        try:
            usuario = UsuarioCli.objects.get(correo_us=correo_us)
            if check_password(password, usuario.pass_us):
                return usuario
        except UsuarioCli.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UsuarioCli.objects.get(pk=user_id)
        except UsuarioCli.DoesNotExist:
            return None
