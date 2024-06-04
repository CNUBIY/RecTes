from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from .models import DiaHorario,HorasDia, UsuarioCli, GenerosCli, CitaSol
from django.contrib import messages
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
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
    horariobdd = DiaHorario.objects.all()
    horabdd=HorasDia.objects.all()
    citabdd=CitaSol.objects.all()
    return render(request, 'adci_inicio.html', {'horarios':horariobdd,'horas':horabdd,'citas':citabdd})

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

            # Procesar la actualización de la cita con los valores obtenidos
            cita = get_object_or_404(CitaSol, pk=id)
            cita.nom_da = nom_da
            cita.telf_da = telf_da
            cita.fech_da = fech_da
            cita.time_da = time_da
            cita.cort_da = cort_da
            cita.save()

            return redirect('/adci_fechacitas')
        except MultiValueDictKeyError as e:
            # Manejo de error cuando no se encuentra un campo esperado en request.POST
            return HttpResponseBadRequest(f"Missing parameter: {e}")
    else:
        return redirect('/error_p')

#Página HORARIOS Administrador FINAL


#Página CONTABILIDAD Administrador INICIO|

def addcont_adci(request, id):
    citabdd=CitaSol.objects.all()
    return render(request,'adci_addcont.html',{'citas':citabdd})


#Página CONTABILIDAD Administrador FINAl|


#Página error Inicio
def error_p (request):
    return render(request, 'error_page.html')
#Página error FINAL
