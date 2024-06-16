from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from .models import DiaHorario,HorasDia, UsuarioCli, CitaSol, FactCitas
from django.contrib import messages
from datetime import datetime, timedelta, time
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from collections import defaultdict
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.decorators import method_decorator
from Aplicaciones.Citas.middleware import login_required as custom_login_required
from collections import defaultdict, OrderedDict
# Create your views here.

#Página Informativa INICIO
def index (request):
    return render(request,'index.html')


#Página Informativa FINAL


#Página REGISTER usuarios INICIO
@login_required
@custom_login_required
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este correo ya está registrado')
        else:
            user = User.objects.create_user(username=username, password=password)  # Añadir el correo electrónico aquí
            user.save()
            messages.success(request, 'Cuenta creada exitosamente')
            return redirect('/login')
    return render(request, 'usci_register.html')


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
            return redirect("/adci_inicio")
        else:
            messages.error(request, 'Contraseña/Correo Incorrectos')
    return render(request, 'usci_login.html')


def user_logout(request):
    logout (request)
    return redirect('/')


#Página LOGIN usarios FINAL

#Página Inicio Usuarios-Citas INICIO
@login_required
def usci_inicio (request):
    return render(request,'usci_inicio.html')
#Página Inicio Usuarios-Citas FINAL


#Página PERFIL usuarios-citas Inicio

#Página PERFIL usuarios-citas final

#Página PERFIL admin Inicio
@login_required
@custom_login_required
def adci_perfil(request):
    return render(request,'adci_perfil.html')
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

    context = {
        'citas_hoy': citas_hoy,
        'citas_mañana': citas_mañana,
        'citas': todas_citas,
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

            messages.success(request, "Cita actualizada correctamente.")
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
def aggagenda_adci(request):
    if request.method == 'POST':
        try:
            nom_da = request.POST["nom_da"]
            telf_da = request.POST["telf_da"]
            fech_da = request.POST["fech_da"]
            time_da = request.POST["time_da"]
            cort_da = request.POST.get("cort_da") == "on"

            # Validar que el horario esté dentro de los rangos permitidos (8am - 8pm)
            selected_time = datetime.strptime(time_da, "%H:%M").time()
            if not ((8 <= selected_time.hour < 13) or (16 <= selected_time.hour < 20)):
                messages.error(request, "No puede ingresar horarios fuera de servicio.")
                return redirect('/adci_fechacitas')

            # Validar que no se pueda seleccionar una hora pasada para la fecha actual
            current_datetime = datetime.now()
            selected_datetime = datetime.strptime(f"{fech_da} {time_da}", "%Y-%m-%d %H:%M")
            if fech_da == current_datetime.strftime("%Y-%m-%d") and selected_datetime < current_datetime - timedelta(hours=1):
                messages.error(request, "No puedes seleccionar una hora pasada para la fecha de hoy.")
                return redirect('/adci_fechacitas')

            # Verificar si la fecha y hora ya están registradas en otra cita
            citas_existentes = CitaSol.objects.filter(fech_da=fech_da, time_da=time_da)
            if citas_existentes.exists():
                messages.error(request, "Ya existe una cita registrada para esta fecha y hora.")
                return redirect('/adci_fechacitas')

            # Procesar la creación de la cita si pasa todas las validaciones
            nueva_cita = CitaSol.objects.create(
                fech_da=fech_da,
                telf_da=telf_da,
                nom_da=nom_da,
                time_da=time_da,
                cort_da=cort_da,
                est_da=False,
            )
            messages.success(request, "Cita registrada correctamente.")
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
            messages.success(request, "Cita actualizada correctamente.")
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
    factbdd=FactCitas.objects.all()
    citabdd=CitaSol.objects.all()
    return render(request,'cont_inicio.html',{'facturas':factbdd,'citas':citabdd})

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

    total_anual = 0
    for fact in factbdd:
        if fact.fechfac and fact.fechfac.est_da:
            turno = 'matutina' if fact.fechfac.time_da < time(12) else 'vespertina'
            citas_por_fecha[fact.fechfac.fech_da][turno]['ventas'] += fact.valfac
            if fact.fechfac.fech_da.year == datetime.now().year:  # Verificar si la fecha es del año actual
                total_anual += fact.valfac

    # Ordenar citas_por_fecha por fech_da de más actual a más antigua
    citas_por_fecha_ordenadas = OrderedDict(
        sorted(citas_por_fecha.items(), key=lambda item: item[0], reverse=True)
    )

    # Crear un diccionario para el total anual
    totales = {
        'total_anual': total_anual
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
