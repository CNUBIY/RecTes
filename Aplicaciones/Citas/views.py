from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from .models import DiaHorario,HorasDia, UsuarioCli, GenerosCli, CitaSol, FactCitas
from django.contrib import messages
from datetime import datetime, timedelta, time
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from collections import defaultdict
# Create your views here.

#Página Informativa INICIO
def index (request):
    return render(request,'index.html')


#Página Informativa FINAL


#Página REGISTER usuarios INICIO

def usci_reg(request):
    userbdd=UsuarioCli.objects.all()
    genbdd=GenerosCli.objects.all()
    return render(request,'usci_register.html',{'usuarios':userbdd,'generos':genbdd})

def usci_addreg(request):
    id_gen=request.POST["id_gen"]
    genselect=GenerosCli.objects.get(id=id_gen)
    nombre_us=request.POST["nombre_us"]
    apellido_us=request.POST["apellido_us"]
    correo_us=request.POST["correo_us"]
    pass_us=request.POST["pass_us"]

    hashed_password = make_password(pass_us)
    newuser=UsuarioCli.objects.create(
        gen_us=genselect,
        nombre_us=nombre_us,
        apellido_us=apellido_us,
        correo_us=correo_us,
        pass_us=hashed_password,
    )
    messages.success(request, 'Registro exitoso')
    return redirect('/usci_inicio')

def check_email_exists(request):
    email = request.GET.get('correo_us', None)
    if UsuarioCli.objects.filter(correo_us=email).exists():
        return JsonResponse({'exists': True})
    else:
        return JsonResponse({'exists': False})

#Página INICIO usuario FINAL

#Página LOGIN usarios INICIO


def usci_login(request):
    if request.method == 'POST':
        correo_us = request.POST.get('correo_us')
        pass_us = request.POST.get('pass_us')

        mensaje_error = {}

        try:
            usuario = UsuarioCli.objects.get(correo_us=correo_us)
            if not check_password(pass_us, usuario.pass_us):
                mensaje_error['pass_us'] = 'Contraseña incorrecta'
        except UsuarioCli.DoesNotExist:
            mensaje_error['correo_us'] = 'Correo no encontrado'

        if mensaje_error:
            return render(request, 'usci_login.html', {'mensaje_error': mensaje_error})

        user = authenticate(request, correo_us=correo_us, password=pass_us)
        if user is not None:
            login(request, user)
            return redirect('/usci_inicio')  # Redirigir al usuario a la página de inicio
        else:
            mensaje_error['error_login'] = 'Credenciales de inicio de sesión incorrectas'
            return render(request, 'usci_login.html', {'mensaje_error': mensaje_error})

    return render(request, 'usci_login.html')



#Página LOGIN usarios FINAL

#Página Inicio Usuarios-Citas INICIO
@login_required
def usci_inicio (request):
    return render(request,'usci_inicio.html')
#Página Inicio Usuarios-Citas FINAL


#Página PERFIL usuarios-citas Inicio
def usci_perfil(request):
    return render(request,'usci_perfil.html')
#Página PERFIL usuarios-citas final

#Página PERFIL admin Inicio
def adci_perfil(request):
    return render(request,'adci_perfil.html')
#Página PERFIL admin final

#Página Inicio Administrador-Citas GENERAL INICIO
def adci_inicio(request):
    hoy = datetime.now().date()
    dia_semana = hoy.weekday()  # 0 = Lunes, 6 = Domingo

    if dia_semana == 5:  # Si hoy es sábado
        mañana = hoy + timedelta(days=2)  # Muestra el lunes
    else:
        mañana = hoy + timedelta(days=1)

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

def procesarActualizacionHorarioIn(request,id):
    if request.method == 'POST':
        try:
            nom_da = request.POST["nom_da"]
            telf_da = request.POST["telf_da"]
            fech_da = request.POST["fech_da"]
            time_da = request.POST["time_da"]
            cort_da = request.POST.get("cort_da") == "on"


            # Procesar la actualización de la cita con los valores obtenidos
            cita = get_object_or_404(CitaSol, pk=id)
            cita.nom_da = nom_da
            cita.telf_da = telf_da
            cita.fech_da = fech_da
            cita.time_da = time_da
            cita.cort_da = cort_da
            cita.save()

            return redirect('/adci_inicio')
        except MultiValueDictKeyError as e:
            # Manejo de error cuando no se encuentra un campo esperado en request.POST
            return HttpResponseBadRequest(f"Missing parameter: {e}")
    else:
        return redirect('/error_p')

def delete_adciIn(request,id):
    eliminarDiaHorario=CitaSol.objects.get(id=id)
    eliminarDiaHorario.delete()
    return redirect('/adci_inicio')

#Página Inicio Administrador-Citas GENERAL FINAL


#Página HORARIOS Administrador Inicio

def adci_fechacitas (request):
    horariobdd=DiaHorario.objects.all()
    horabdd=HorasDia.objects.all()
    citabdd=CitaSol.objects.all()
    return render(request,'adci_fechacitas.html',{'horarios':horariobdd,'horas':horabdd,'citas':citabdd})

def aggagenda_adci(request):
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


def delete_adci(request,id):
    eliminarDiaHorario=CitaSol.objects.get(id=id)
    eliminarDiaHorario.delete()
    return redirect('/adci_fechacitas')

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
            else:
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



def check_appointment(request):
    if request.method == 'POST':
        fecha = request.POST.get('fech_da')
        hora = request.POST.get('time_da')

        exists = CitaSol.objects.filter(fech_da=fecha, time_da=hora).exists()

        return JsonResponse({'exists': exists})

#Página HORARIOS Administrador FINAL


#Página CONTABILIDAD Administrador INICIO|
def cont_inicio(request):
    factbdd=FactCitas.objects.all()
    citabdd=CitaSol.objects.all()
    return render(request,'cont_inicio.html',{'facturas':factbdd,'citas':citabdd})

def addcont_adci(request, id):
    citabdd=get_object_or_404(CitaSol,id=id)
    factbdd=FactCitas.objects.all()
    return render(request,'adci_addcont.html',{'cita':citabdd,'facts':factbdd})

def cont_int(request):
    citabdd = CitaSol.objects.all()  # Obtener todas las citas
    factbdd = FactCitas.objects.all()

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

    for fact in factbdd:
        if fact.fechfac.est_da:  # Solo considerar las citas con est_da=True
            turno = 'matutina' if fact.fechfac.time_da < time(12) else 'vespertina'
            citas_por_fecha[fact.fechfac.fech_da][turno]['ventas'] += fact.valfac

    context = {
        'citas_por_fecha': dict(citas_por_fecha)  # Convertir defaultdict a dict
    }

    return render(request, 'cont_int.html', context)


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

def cont_vac(request):
    factbdd=FactCitas.objects.all()
    return render(request,'add_vac.html')

#Página CONTABILIDAD Administrador FINAl|


#Página error Inicio
def error_p (request):
    return render(request, 'error_page.html')
#Página error FINAL
