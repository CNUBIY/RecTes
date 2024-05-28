from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import DiaHorario,HorasDia, UsuarioCli, GenerosCli
from django.contrib import messages
from datetime import datetime, timedelta
# Create your views here.

#Página Informativa INICIO
def index (request):
    return render(request,'index.html')


#Página Informativa FINAL

#Página Inicio Usuarios-Citas INICIO
def usci_inicio (request):
    return render(request,'usci_inicio.html')
#Página Inicio Usuarios-Citas FINAL

#Página REGISTER usuarios INICIO

def usci_reg(request):
    userbdd=UsuarioCli.objects.all()
    genbdd=GenerosCli.objects.all()
    return render(request,'usci_register.html',{'usuarios':userbdd,'generos':genbdd})

#Página INICIO usuario FINAL

#Página LOGIN usarios INICIO
def usci_login(request):

    if request.method == 'POST':
        correo_us = request.POST.get('correo_us')
        pass_us = request.POST.get('pass_us')

        mensaje_error = {}

        try:
            usuario = UsuarioCli.objects.get(correo_us=correo_us)
            if pass_us != usuario.pass_us:
                mensaje_error['pass_us'] = 'Contraseña incorrecta'
        except UsuarioCli.DoesNotExist:
            mensaje_error['correo_us'] = 'Correo no encontrado'

        if mensaje_error:
            return render(request, 'usci_login.html', {'mensaje_error': mensaje_error})

        return redirect('/usci_inicio')

    return render(request, 'usci_login.html')

#Página LOGIN usarios FINAL

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
    return render(request, 'adci_inicio.html', {'horarios':horariobdd})

#Página Inicio Administrador-Citas GENERAL FINAL


#Página HORARIOS Administrador Inicio

def adci_fechacitas (request):
    horariobdd=DiaHorario.objects.all()
    horabdd=HorasDia.objects.all()
    return render(request,'adci_fechacitas.html',{'horarios':horariobdd,'horas':horabdd})

def aggagenda_adci(request):
    diaH=request.POST["diaH"]
    id_hora=request.POST.getlist("id_hora")


    for hora_id in id_hora:
        horaSelec = HorasDia.objects.get(id=hora_id)
        nuevoHorarioDia = DiaHorario.objects.create(
        diaH=diaH,
        horario=horaSelec,
        estado=False,
        )
    return redirect('/adci_fechacitas')

def aggsem_adci(request):
    id_hora = request.POST.getlist("id_hora")

    # Obtener la fecha actual
    diaH_date = datetime.now().date()

    # Calcular los días hábiles restantes hasta el viernes
    current_weekday = diaH_date.weekday()
    days_until_friday = 4 - current_weekday  # 4 es viernes

    # Si el día actual es sábado (5) o domingo (6), ajustar a lunes de la próxima semana
    if current_weekday > 4:
        days_until_monday = 7 - current_weekday  # Ajustar a lunes de la próxima semana
        diaH_date = diaH_date + timedelta(days=days_until_monday)  # Mover al próximo lunes
        current_weekday= diaH_date.weekday()

    days_until_friday= 4 - current_weekday

    # Crear registros para cada día hábil desde el día actual hasta el viernes
    for day in range(days_until_friday + 1):
        current_date = diaH_date + timedelta(days=day)
        if current_date.weekday() > 4:
            continue  # Ignorar sábados y domingos
        for hora_id in id_hora:
            horaSelec = HorasDia.objects.get(id=hora_id)
            DiaHorario.objects.create(
                diaH=current_date,
                horario=horaSelec,
                estado=False,
            )

    return redirect('/adci_fechacitas')

def delete_adci(request,id):
    eliminarDiaHorario=DiaHorario.objects.get(id=id)
    eliminarDiaHorario.delete()
    return redirect('/adci_fechacitas')

def procesarActualizacionHorario(request,id):
    id=request.POST["data_id"]
    diaH=request.POST["diaH"]
    id_hora=request.POST["id_hora"]
    horaSelec=HorasDia.objects.get(id=id_hora)

    horario=DiaHorario.objects.get(id=id)
    horario.diaH=diaH
    horario.horario=horaSelec
    horario.estado=False
    horario.save()
    return redirect('/adci_fechacitas')

#Página HORARIOS Administrador FINAL
