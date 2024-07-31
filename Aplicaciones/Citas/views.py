from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from .models import DiaHorario,HorasDia, UsuarioCli, CitaSol, FactCitas
from django.contrib import messages
from datetime import datetime, timedelta, time
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from collections import defaultdict
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.utils.decorators import method_decorator
from Aplicaciones.Citas.middleware import login_required as custom_login_required
from collections import defaultdict, OrderedDict
import telegram
import asyncio
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.conf import settings
from telegram import Bot
from asgiref.sync import async_to_sync
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import random
import string
from django.core.mail import send_mail
# Create your views here.


my_token = settings.BOT_TOKEN
my_chat_id = settings.BOT_CHAT_ID

async def send_telegram_message(msg, chat_id=my_chat_id, token=my_token):
    bot_instance = Bot(token=token)
    await bot_instance.send_message(chat_id=chat_id, text=msg)

# Página Informativa INICIO
async def index(request):
    return render(request, 'index.html')
# Página Informativa FINAL


#Página REGISTER usuarios INICIO

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

@login_required
@custom_login_required
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este correo ya está registrado')
        else:
            verification_code = generate_verification_code()

            # Guardar el código de verificación en la sesión
            request.session['verification_code'] = verification_code
            request.session['username'] = username
            request.session['password'] = password

            # Enviar correo de verificación
            send_mail(
                'Código de Verificación',
                f'Tu código de verificación es: {verification_code}',
                settings.EMAIL_HOST_USER,
                [username],
                fail_silently=False,
            )

            messages.success(request, 'Cuenta creada correctamente. Revisa tu correo para el código de verificación.')
            return redirect('verify')
    return render(request, 'usci_register.html')

@login_required
@custom_login_required
def verify_email(request):
    if request.method == 'POST':
        code = request.POST['code']
        username = request.session.get('username')
        password = request.session.get('password')
        verification_code = request.session.get('verification_code')

        if code == verification_code:
            user = User.objects.create_user(username=username, password=password)
            user.email_verified = True
            user.save()

            # Limpiar la sesión
            del request.session['verification_code']
            del request.session['username']
            del request.session['password']

            messages.success(request, 'Correo verificado exitosamente.')
            return redirect('/login/')
        else:
            messages.error(request, 'Código de verificación incorrecto.')

    return render(request, 'usci_verify.html')

#Página INICIO usuario FINAL

#Página LOGIN usarios INICIO

def user_login(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['last_activity'] = timezone.now().isoformat()  # Convertir a cadena
            async_to_sync(send_telegram_message)(f"Se ha iniciado sesión con {user.username} en Sitio administrativo Secretaría")
            return redirect("/adci_inicio")
        else:
            messages.error(request, 'Contraseña/Correo Incorrectos')
    return render(request, 'usci_login.html')

def request_reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(username=email).exists():
            verification_code = generate_verification_code()

            # Guardar el código de verificación en la sesión
            request.session['reset_password_code'] = verification_code
            request.session['reset_email'] = email

            # Enviar correo de verificación
            send_mail(
                'Código de Restablecimiento de Contraseña',
                f'Tu código de restablecimiento de contraseña es: {verification_code}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Revisa tu correo para el código de restablecimiento de contraseña.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Este correo no está registrado.')
            return redirect('request_reset_password')
    return render(request, 'usci_requestemail.html')

def reset_password(request):
    if request.method == 'POST':
        code = request.POST['code']
        new_password = request.POST['new_password']
        email = request.session.get('reset_email')
        verification_code = request.session.get('reset_password_code')

        if code == verification_code:
            user = User.objects.get(username=email)
            user.set_password(new_password)
            user.save()

            # Limpiar la sesión
            del request.session['reset_password_code']
            del request.session['reset_email']

            messages.success(request, 'Contraseña restablecida exitosamente.')
            return redirect('login')
        else:
            messages.error(request, 'Código de verificación incorrecto.')
    return render(request, 'usci_resetp.html')

def user_logout(request):
    logout (request)
    return redirect('/')


#Página LOGIN usarios FINAL

#Página Inicio Usuarios-Citas INICIO
@login_required
def usci_inicio (request):
    return render(request,'usci_inicio.html')
#Página Inicio Usuarios-Citas FINAL

#Página PERFIL admin Inicio
@login_required
@custom_login_required
def adci_perfil(request):
    # Obtener todos los usuarios registrados con información básica incluyendo is_staff e is_superuser
    usuarios = User.objects.all().values('id', 'username', 'date_joined', 'last_login', 'is_staff', 'is_superuser')

    # Pasar información del usuario actual
    usuario_actual = request.user
    es_staff = usuario_actual.is_staff
    es_superuser = usuario_actual.is_superuser

    # Manejar el cambio de contraseña
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para mantener la sesión después de cambiar la contraseña
            messages.success(request, '¡Tu contraseña ha sido actualizada exitosamente!')
            return redirect('adci_perfil')
        else:
            messages.error(request,'Contraseña incorrecta')

    return render(request, 'adci_perfil.html', {
        'usuarios': usuarios,
        'es_staff': es_staff,
        'es_superuser': es_superuser,
    })


@login_required
@permission_required('auth.delete_user', raise_exception=True)
def eliminar_usuario(request, user_id):
    usuario_a_eliminar = get_object_or_404(User, id=user_id)

    if usuario_a_eliminar.is_staff or usuario_a_eliminar.is_superuser:
        messages.error(request, 'No tienes permiso para eliminar este usuario.')
    else:
        usuario_a_eliminar.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')

    return redirect('adci_perfil')


@login_required
@custom_login_required
def promote_user_to_admin(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        admin_password = request.POST.get('admin_password')

        # Verificar la contraseña del usuario actual
        user = authenticate(username=request.user.username, password=admin_password)
        if user is not None and user.is_staff:
            try:
                user_to_promote = get_object_or_404(User, id=user_id)
                admin_group = Group.objects.get(name='Administradores')
                user_to_promote.is_staff = True
                user_to_promote.groups.add(admin_group)
                user_to_promote.save()
                messages.success(request, f'{user_to_promote.username} ha sido promovido a Administrador exitosamente.')
            except User.DoesNotExist:
                messages.error(request, 'Usuario no encontrado.')
            except Group.DoesNotExist:
                messages.error(request, 'Grupo de Administradores no encontrado.')
        else:
            messages.error(request, 'Contraseña incorrecta')

    return redirect('adci_perfil')

@login_required
@custom_login_required
def delete_account(request):
    if request.method == 'POST':
        delete_password = request.POST.get('delete_password')

        # Verificar la contraseña del usuario actual
        user = authenticate(username=request.user.username, password=delete_password)
        if user is not None and not user.is_superuser:
            user.delete()
            messages.success(request, 'Tu cuenta ha sido eliminada exitosamente.')
            return redirect('login')  # Redirigir al logout después de eliminar la cuenta
        else:
            messages.error(request, 'Contraseña incorrecta o no puedes eliminar una cuenta de superusuario.')

    return redirect('adci_perfil')

#Página PERFIL admin final

#Página Inicio Administrador-Citas GENERAL INICIO
@login_required
@custom_login_required
def adci_inicio(request):
    hoy = datetime.now().date()
    dia_semana = hoy.weekday()  # 0 = Lunes, 6 = Domingo

    if dia_semana == 5:  # Si hoy es sábado
        mañana = hoy + timedelta(days=2)  # Muestra el lunes
    else:
        mañana = hoy + timedelta(days=1)

    # Eliminar las citas no confirmadas y no cortas para fechas pasadas
    CitaSol.objects.filter(est_da=False, cort_da=False, fech_da__lt=hoy).delete()

    # Ordenar las citas por el campo 'time_da'
    citas_hoy = CitaSol.objects.filter(fech_da=hoy, cort_da=False).order_by('time_da')
    citas_mañana = CitaSol.objects.filter(fech_da=mañana).order_by('time_da')
    todas_citas = CitaSol.objects.all().order_by('fech_da', 'time_da')

    # Formatear las horas de las citas para mañana
    for cita in citas_mañana:
        cita.formatted_time = cita.time_da.strftime('%I:%M %p')

    # Obtener citas que están a un día de llegar
    citas_proximas = CitaSol.objects.filter(fech_da=hoy + timedelta(days=1), cort_da=False).order_by('time_da')

    context = {
        'citas_hoy': citas_hoy,
        'citas_mañana': citas_mañana,
        'citas': todas_citas,
        'citas_proximas': citas_proximas,  # Pasar las citas próximas al contexto
        'mañana': mañana,
    }

    return render(request, 'adci_inicio.html', context)


@login_required
@custom_login_required
def aggin_adci(request):
    nom_da=request.POST["nom_da"]
    telf_da=request.POST["telf_da"]
    fech_da=request.POST["fech_da"]
    time_da=request.POST["time_da"]
    cort_da = request.POST.get("cort_da") == "on"

    nuevoHorarioDia = CitaSol.objects.create(
    fech_da=fech_da,
    telf_da=telf_da,
    nom_da=nom_da,
    time_da=time_da,
    cort_da=cort_da,
    est_da=False,
    )
    return redirect('/adci_inicio')

@login_required
@custom_login_required
def procesarActualizacionHorarioIn(request, id):
    if request.method == 'POST':
        try:
            nom_da = request.POST["nom_da"]
            telf_da = request.POST["telf_da"]
            fech_da = request.POST["fech_da"]
            time_da = request.POST["time_da"]
            cort_da = request.POST.get("cort_da") == "on"

            #horarios de servicio
            selected_datetime = datetime.strptime(f"{fech_da} {time_da}", "%Y-%m-%d %H:%M")
            selected_time = selected_datetime.time()
            if not ((8 <= selected_time.hour < 13) or (16 <= selected_time.hour < 20)):
                messages.error(request, "No puede ingresar horarios fuera de servicio.")
                return redirect('/adci_inicio')

            # horas pasadas
            current_datetime = datetime.now()
            if fech_da == current_datetime.strftime("%Y-%m-%d") and selected_datetime < current_datetime - timedelta(hours=1):
                messages.error(request, "No puedes seleccionar una hora pasada para la fecha de hoy.")
                return redirect('/adci_inicio')

            # fechas registradas
            citas_existentes = CitaSol.objects.filter(fech_da=fech_da, time_da=time_da).exclude(pk=id)
            if citas_existentes.exists():
                messages.error(request, "Ya existe una cita registrada para esta fecha y hora.")
                return redirect('/adci_inicio')

            cita = get_object_or_404(CitaSol, pk=id)
            cita.nom_da = nom_da
            cita.telf_da = telf_da
            cita.fech_da = fech_da
            cita.time_da = time_da
            cita.cort_da = cort_da
            cita.save()

            messages.success(request, "Cita actualizada exitosamente.")
            return redirect('/adci_inicio')
        except MultiValueDictKeyError as e:
            # Manejo de error cuando no se encuentra un campo esperado en request.POST
            return HttpResponseBadRequest(f"Missing parameter: {e}")
        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            messages.error(request, "Ha ocurrido un error al procesar la solicitud.")
            return redirect('/error_p')
    else:
        return redirect('/error_p')

@login_required
@custom_login_required
def delete_adciIn(request,id):
    eliminarDiaHorario=CitaSol.objects.get(id=id)
    eliminarDiaHorario.delete()
    return redirect('/adci_inicio')

#Página Inicio Administrador-Citas GENERAL FINAL


#Página HORARIOS Administrador Inicio

@login_required
@custom_login_required
def adci_fechacitas (request):
    horariobdd=DiaHorario.objects.all()
    horabdd=HorasDia.objects.all()
    citabdd=CitaSol.objects.all()
    return render(request,'adci_fechacitas.html',{'horarios':horariobdd,'horas':horabdd,'citas':citabdd})
@login_required
@custom_login_required
def verificar_cita(request):
    fecha = request.GET.get('fecha')
    hora = request.GET.get('hora')
    id_cita = request.GET.get('id_cita')

    if id_cita:
        # Excluir la cita actual de la verificación
        existe = CitaSol.objects.filter(fech_da=fecha, time_da=hora).exclude(id=id_cita).exists()
    else:
        # Verificar sin excluir ninguna cita
        existe = CitaSol.objects.filter(fech_da=fecha, time_da=hora).exists()

    return JsonResponse({'existe': existe})

@login_required
@custom_login_required
def aggagenda_adci(request):
    if request.method == 'POST':
        try:
            nom_da = request.POST["nom_da"]
            telf_da = request.POST["telf_da"]
            fech_da = request.POST["fech_da"]
            time_da = request.POST["time_da"]
            cort_da = request.POST.get("cort_da") == "on"

            # Procesar la creación de la cita si pasa todas las validaciones
            nueva_cita = CitaSol.objects.create(
                fech_da=fech_da,
                telf_da=telf_da,
                nom_da=nom_da,
                time_da=time_da,
                cort_da=cort_da,
                est_da=False,
            )
            messages.success(request, "Cita registrada exitosamente.")
            return redirect('/adci_inicio')

        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            messages.error(request, "Ha ocurrido un error al procesar la solicitud.")
            return redirect('/error_p')
    else:
        # Manejar solicitudes GET o cualquier otro método HTTP no permitido
        return redirect('/error_p')

@login_required
@custom_login_required
def delete_adci(request,id):
    eliminarDiaHorario=CitaSol.objects.get(id=id)
    eliminarDiaHorario.delete()
    return redirect('/adci_fechacitas')

@login_required
@custom_login_required
def procesarActualizacionHorario(request, id):
    if request.method == 'POST':
        try:
            nom_da = request.POST["nom_da"]
            telf_da = request.POST["telf_da"]
            fech_da = request.POST["fech_da"]
            time_da = request.POST["time_da"]
            cort_da = request.POST.get("cort_da") == "on"

            # Verificar si la fecha y hora ya están registradas en otra cita
            citas_existentes = CitaSol.objects.exclude(pk=id).filter(fech_da=fech_da, time_da=time_da)
            if citas_existentes.exists():
                # Mostrar mensaje de error si la cita ya existe
                messages.error(request, "No puede seleccionar una fecha y hora ya registrada.")
                return redirect('/adci_fechacitas')

            # Validar que la hora no sea en el pasado para la fecha actual
            current_datetime = datetime.now()
            selected_datetime = datetime.strptime(f"{fech_da} {time_da}", "%Y-%m-%d %H:%M")
            if fech_da == current_datetime.strftime("%Y-%m-%d") and selected_datetime.time() < current_datetime.time():
                messages.error(request, "No puedes seleccionar una hora pasada para la fecha de hoy.")
                return redirect('/adci_fechacitas')

            # Validar que el horario esté dentro de los rangos permitidos
            selected_time = selected_datetime.time()
            if not ((8 <= selected_time.hour < 13) or (16 <= selected_time.hour < 20) or (selected_time.hour == 13 and selected_time.minute == 0) or (selected_time.hour == 20 and selected_time.minute == 0)):
                messages.error(request, "El horario debe estar entre 8am-1pm o 4pm-8pm.")
                return redirect('/adci_fechacitas')

            # Procesar la actualización de la cita con los valores obtenidos
            cita = get_object_or_404(CitaSol, pk=id)
            cita.nom_da = nom_da
            cita.telf_da = telf_da
            cita.fech_da = fech_da
            cita.time_da = time_da
            cita.cort_da = cort_da
            cita.save()

            # Agregar mensaje de éxito si la actualización fue exitosa
            messages.success(request, "Cita actualizada exitosamente.")
            return redirect('/adci_fechacitas')
        except MultiValueDictKeyError as e:
            # Manejo de error cuando no se encuentra un campo esperado en request.POST
            return HttpResponseBadRequest(f"Missing parameter: {e}")
    else:
        return redirect('/error_p')


@login_required
@custom_login_required
def check_appointment(request):
    if request.method == 'POST':
        fecha = request.POST.get('fech_da')
        hora = request.POST.get('time_da')

        exists = CitaSol.objects.filter(fech_da=fecha, time_da=hora).exists()

        return JsonResponse({'exists': exists})

#Página HORARIOS Administrador FINAL


#Página CONTABILIDAD Administrador INICIO|
@login_required
@custom_login_required
def cont_inicio(request):
    factbdd = FactCitas.objects.all()
    citabdd = CitaSol.objects.all()
    total_anual = 0
    total_primer_semestre = 0
    total_segundo_semestre = 0
    citas_por_fecha = {}

    for fact in factbdd:
        if fact.fechfac and fact.fechfac.est_da:
            fecha = fact.fechfac.fech_da
            turno = 'matutina' if fact.fechfac.time_da < time(12) else 'vespertina'

            if fecha not in citas_por_fecha:
                citas_por_fecha[fecha] = {'matutina': {'ventas': 0}, 'vespertina': {'ventas': 0}}

            citas_por_fecha[fecha][turno]['ventas'] += fact.valfac

            # Verificar si la fecha es del año actual
            if fecha.year == datetime.now().year:
                total_anual += fact.valfac

                # Calcular los totales semestrales
                if 1 <= fecha.month <= 6:
                    total_primer_semestre += fact.valfac
                elif 7 <= fecha.month <= 12:
                    total_segundo_semestre += fact.valfac

    # Crear un diccionario para el total anual y los totales semestrales
    totales = {
        'total_anual': total_anual,
        'total_primer_semestre': total_primer_semestre,
        'total_segundo_semestre': total_segundo_semestre
    }

    return render(request, 'cont_inicio.html', {'facturas': factbdd, 'citas': citabdd, 'totales': totales})

@login_required
@custom_login_required
def addcont_adci(request, id):
    citabdd=get_object_or_404(CitaSol,id=id)
    factbdd=FactCitas.objects.all()
    return render(request,'adci_addcont.html',{'cita':citabdd,'facts':factbdd})

@login_required
@custom_login_required
def cont_int(request):
    # Obtener todas las citas y facturas
    citabdd = CitaSol.objects.all()
    factbdd = FactCitas.objects.all()

    # Crear un diccionario para almacenar las citas por fecha
    citas_por_fecha = defaultdict(lambda: {
        'matutina': {'atendidos': 0, 'ventas': 0, 'cortesias': 0},
        'vespertina': {'atendidos': 0, 'ventas': 0, 'cortesias': 0}
    })

    for cita in citabdd:
        turno = 'matutina' if cita.time_da < time(12) else 'vespertina'
        if cita.cort_da:
            citas_por_fecha[cita.fech_da][turno]['cortesias'] += 1
        if cita.est_da:
            citas_por_fecha[cita.fech_da][turno]['atendidos'] += 1

    # Ordenar citas_por_fecha por fech_da de más actual a más antigua
    citas_por_fecha_ordenadas = OrderedDict(
        sorted(citas_por_fecha.items(), key=lambda item: item[0], reverse=True)
    )

    total_anual = 0
    total_primer_semestre = 0
    total_segundo_semestre = 0

    for fact in factbdd:
        if fact.fechfac and fact.fechfac.est_da:
            turno = 'matutina' if fact.fechfac.time_da < time(12) else 'vespertina'
            citas_por_fecha[fact.fechfac.fech_da][turno]['ventas'] += fact.valfac

            # Verificar si la fecha es del año actual
            if fact.fechfac.fech_da.year == datetime.now().year:
                total_anual += fact.valfac

                # Calcular los totales semestrales
                if 1 <= fact.fechfac.fech_da.month <= 6:
                    total_primer_semestre += fact.valfac
                elif 7 <= fact.fechfac.fech_da.month <= 12:
                    total_segundo_semestre += fact.valfac

    # Crear un diccionario para el total anual y los totales semestrales
    totales = {
        'total_anual': total_anual,
        'total_primer_semestre': total_primer_semestre,
        'total_segundo_semestre': total_segundo_semestre
    }

    context = {
        'citas_por_fecha': citas_por_fecha_ordenadas,
        'totales': totales  # Agregar el total anual al contexto
    }

    return render(request, 'cont_int.html', context)


@login_required
@custom_login_required
def aggcont_adci(request):
    if request.method == 'POST':
        id_fech = request.POST["id_fech"]
        idfac = request.POST["idfac"]
        descfac = request.POST["descfac"]
        valfac = request.POST["valfac"]
        obsfac = request.POST["obsfac"]


        nueva_factura = FactCitas.objects.create(
            fechfac=CitaSol.objects.get(id=id_fech),  # Asociar la factura con la cita
            idfac=idfac,
            descfac=descfac,
            valfac=valfac,
            obsfac=obsfac,
        )

        # Cambiar est_da a True en CitaSol
        cita = get_object_or_404(CitaSol, id=id_fech)
        cita.est_da = True
        cita.save()

        return redirect('/adci_inicio')

    return redirect('/adci_inicio')

@login_required
@custom_login_required
def cont_vac(request):
    factbdd=FactCitas.objects.all()
    return render(request,'add_vac.html')


@login_required
@custom_login_required
def aggcont_vac(request):
    if request.method == "POST":
        idfac = request.POST.get("idfac")
        descfac = request.POST.get("descfac")
        valfac = request.POST.get("valfac")
        obsfac = request.POST.get("obsfac")

        if idfac and descfac and valfac and obsfac:
            nueva_vacuna = FactCitas.objects.create(
                idfac=idfac,
                descfac=descfac,
                valfac=valfac,
                obsfac=obsfac,
            )
            return redirect('/adci_inicio/cont_inicio/')
        else:
            message.error(request,"Faltan datos")
    else:
        redirect('/error_p')

#Página CONTABILIDAD Administrador FINAl|


#Página error Inicio
def error_p (request):
    return render(request, 'error_page.html')
#Página error FINAL
