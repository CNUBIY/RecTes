from django.shortcuts import render, redirect
from .models import CitaDia, NombreDia, DiaHorario,HorasDia
from django.contrib import messages
# Create your views here.

#Página Informativa INICIO
def index (request):
    return render(request,'index.html')


#Página Informativa FINAL

#Página Inicio Usuarios-Citas INICIO
def usci_inicio (request):
    return render(request,'usci_inicio.html')
#Página Inicio Usuarios-Citas FINAL



#Página Inicio Administrador-Citas GENERAL INICIO
def adci_inicio (request):
    return render(request,'adci_inicio.html')


#Página Inicio Administrador-Citas GENERAL FINAL


#Página DIAS Administrador INICIO
def adci_dias (request):
    diabdd=CitaDia.objects.all()
    nombdd=NombreDia.objects.all()
    return render(request,'adci_dias.html',{'dias':diabdd,'nombres':nombdd})

def agg_adci(request):
    fechaCita=request.POST["fechaCita"]
    id_cita = request.POST["id_cita"]
    diaSelec=NombreDia.objects.get(id=id_cita)

    nuevoFechaCita=CitaDia.objects.create(
    fechaCita=fechaCita,
    dia=diaSelec,
    )
    return redirect('/adci_dias')

def del_adci(request,id):
    delDia=CitaDia.objects.get(id=id)
    delDia.delete()
    return redirect('/adci_dias')
#Página DIAS Administrador FINAL



#Página HORARIOS Administrador Inicio

def adci_fechacitas (request):
    horariobdd=DiaHorario.objects.all()
    horabdd=HorasDia.objects.all()
    diahbdd=CitaDia.objects.all()
    return render(request,'adci_fechacitas.html',{'horarios':horariobdd,'horas':horabdd,'dias':diahbdd})

def aggagenda_adci(request):
    id_dia=request.POST["id_dia"]
    diaSelec=CitaDia.objects.get(id=id_dia)
    id_hora=request.POST.getlist("id_hora")


    for hora_id in id_hora:
        horaSelec = HorasDia.objects.get(id=hora_id)
        nuevoHorarioDia = DiaHorario.objects.create(
        diaH=diaSelec,
        horario=horaSelec,
        estado=False,
        )
    return redirect('/adci_fechacitas')

def procesarActualizacionHorario(request,id):
    id=request.POST["data_id"]
    id_dia=request.POST["id_dia"]
    diaSelec=CitaDia.objects.get(id=id_dia)
    id_hora=request.POST["id_hora"]
    horaSelec=HorasDia.objects.get(id=id_hora)

    horario=DiaHorario.objects.get(id=id)
    horario.diah=diaSelec
    horario.horario=horaSelec
    horario.estado=False
    horario.save()
    return redirect('/adci_fechacitas')

#Página HORARIOS Administrador FINAL
