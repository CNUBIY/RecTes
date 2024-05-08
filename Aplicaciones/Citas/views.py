from django.shortcuts import render, redirect
from .models import DiaHorario,HorasDia
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
#
# def procesarActualizacionHorario(request,id):
#     id=request.POST["data_id"]
#     id_dia=request.POST["id_dia"]
#     diaSelec=CitaDia.objects.get(id=id_dia)
#     id_hora=request.POST["id_hora"]
#     horaSelec=HorasDia.objects.get(id=id_hora)
#
#     horario=DiaHorario.objects.get(id=id)
#     horario.diah=diaSelec
#     horario.horario=horaSelec
#     horario.estado=False
#     horario.save()
#     return redirect('/adci_fechacitas')

#Página HORARIOS Administrador FINAL
