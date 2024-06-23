from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
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
from .models import Patient, Gender
# Create your views here.


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
            return redirect("doc_inicio")
        else:
            messages.error(request, 'Contraseña/Correo Incorrectos')
    return render(request, 'auth/doc_login.html')


def user_logout(request):
    logout (request)
    return redirect('/')


#Página LOGIN usarios FINAL

#Página Vista de Historiales INICIO
@login_required
@custom_login_required
def doc_inicio (request):
    histobdd=Patient.objects.all()
    return render(request,'general/doc_inicio.html',{'historiales':histobdd})
#Página Vista de Historiales FINAl



#Página PACIENTES Inicio

@login_required
@custom_login_required
def doc_patient (request,idPat):
    patbdd=Patient.objects.get(idPat=idPat)
    genbdd=Gender.objects.all()
    return render(request, 'histo/patient.html',{'pacientes':patbdd,'generos':genbdd})


#Página PACIENTES FINAL



#Página CREAR PACIENTE INICIO
@login_required
@custom_login_required
def new_patient(request):
    patbdd=Patient.objects.all()
    genbdd=Gender.objects.all()

    if request.method == 'POST':
        try:
            namePat = request.POST['namePat']
            lastnPat = request.POST['lastnPat']
            pldatePat = request.POST['pldatePat']
            birthPat = request.POST['birthPat']
            placePat = request.POST['placePat']
            natiPat = request.POST['natiPat']
            ciPat = request.POST['ciPat']
            id_gen = request.POST['id_gen']
            genselect = Gender.objects.get(id=id_gen)

            new_pat = Patient.objects.create(
                namePat=namePat,
                lastnPat=lastnPat,
                pldatePat=pldatePat,
                birthPat=birthPat,
                placePat=placePat,
                natiPat=natiPat,
                ciPat=ciPat,
                genPat=genselect,
            )
            messages.success(request, "Paciente registrado correctamente.")
            return redirect('doc_inicio')

        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            messages.error(request, "Ha ocurrido un error al procesar la solicitud.")
            return redirect('error_p')

    return render(request,'patients/new.html',{'pacientes':patbdd,'generos':genbdd})


@login_required
@custom_login_required
def edit_patient(request,idPat):
    if request.method=='POST':
        # try:
            idPat=request.POST["idPat"]
            namePat = request.POST['namePat']
            lastnPat = request.POST['lastnPat']
            pldatePat = request.POST['pldatePat']
            birthPat = request.POST['birthPat']
            placePat = request.POST['placePat']
            natiPat = request.POST['natiPat']
            ciPat = request.POST['ciPat']
            id_gen = request.POST['id_gen']
            genselect = Gender.objects.get(id=id_gen)

            patEdit = Patient.objects.get(idPat=idPat)
            patEdit.namePat=namePat
            patEdit.lastnPat=lastnPat
            patEdit.birthPat=birthPat
            patEdit.placePat=placePat
            patEdit.natiPat=natiPat
            patEdit.ciPat=ciPat
            patEdit.genPat=genselect
            patEdit.save()

            messages.success(request, 'Paciente editado exitósamente')
    return redirect('doc_patient', idPat=idPat)
        # except Exception as e:
        #     print(f"Error al procesar la solicitud: {str(e)}")
        #     messages.error(request, "Ha ocurrido un error al procesar la solicitud.")
        #     return redirect('error_p')
#Página CREAR PACIENTE FINAL
