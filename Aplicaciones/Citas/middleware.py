from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

class AutoLogout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = timezone.now()
            last_activity_str = request.session.get('last_activity')

            if last_activity_str:
                last_activity = datetime.fromisoformat(last_activity_str)
                session_expiry_time = last_activity + timedelta(seconds=settings.SESSION_COOKIE_AGE)
                if current_time > session_expiry_time:
                    logout(request)
                else:
                    request.session['last_activity'] = current_time.isoformat()
            else:
                request.session['last_activity'] = current_time.isoformat()

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Redirigir a página de error si el usuario no está autenticado y la vista requiere login
        if not request.user.is_authenticated and hasattr(view_func, 'login_required'):
            return redirect('login')  # Redirige a la vista de error

def login_required(view_func):
    view_func.login_required = True
    return view_func
