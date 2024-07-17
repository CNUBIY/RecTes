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
from .models import Patient, Gender, MadreCita, PadreCita
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
    mombdd=MadreCita.objects.all()
    dadbdd=PadreCita.objects.all()
    # Formatear fechas a YYYY-MM-DD
    for mom in mombdd:
        mom.age_mom = mom.age_mom.strftime('%Y-%m-%d') if mom.age_mom else ''
    for dad in dadbdd:
        dad.age_fat = dad.age_fat.strftime('%Y-%m-%d') if dad.age_fat else ''
    return render(request, 'histo/patient.html',{'pacientes':patbdd,'generos':genbdd,'mom':mombdd, 'dad':dadbdd})


#Página PACIENTES FINAL



#Página CREAR PACIENTE INICIO
@login_required
@custom_login_required
def new_patient(request):
    patbdd = Patient.objects.all()
    genbdd = Gender.objects.all()

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
            tf_casa = request.POST['tf_casa']
            cell = request.POST['cell']
            tf_tra = request.POST['tf_tra']
            seguroPat = 'seguroPat' in request.POST

            new_pat = Patient.objects.create(
                namePat=namePat,
                lastnPat=lastnPat,
                pldatePat=pldatePat,
                birthPat=birthPat,
                placePat=placePat,
                natiPat=natiPat,
                ciPat=ciPat,
                genPat=genselect,
                tf_casa=tf_casa,
                cell=cell,
                tf_tra=tf_tra,
                seguroPat=seguroPat
            )
            messages.success(request, "Paciente registrado correctamente.")
            return redirect('doc_inicio')

        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            messages.error(request, "Ha ocurrido un error al procesar la solicitud.")
            return redirect('error_p')

    return render(request, 'patients/new.html', {'pacientes': patbdd, 'generos': genbdd})

@login_required
@custom_login_required
def edit_patient(request, idPat):
    if request.method == 'POST':
        try:
            idPat = request.POST["idPat"]
            namePat = request.POST['namePat']
            lastnPat = request.POST['lastnPat']
            pldatePat = request.POST['pldatePat']
            birthPat = request.POST['birthPat']
            placePat = request.POST['placePat']
            natiPat = request.POST['natiPat']
            ciPat = request.POST['ciPat']
            id_gen = request.POST['id_gen']
            genselect = Gender.objects.get(id=id_gen)
            tf_casa = request.POST['tf_casa']
            cell = request.POST['cell']
            tf_tra = request.POST['tf_tra']
            seguroPat = 'seguroPat' in request.POST

            patEdit = Patient.objects.get(idPat=idPat)
            patEdit.namePat = namePat
            patEdit.lastnPat = lastnPat
            patEdit.pldatePat = pldatePat
            patEdit.birthPat = birthPat
            patEdit.placePat = placePat
            patEdit.natiPat = natiPat
            patEdit.ciPat = ciPat
            patEdit.genPat = genselect
            patEdit.tf_casa = tf_casa
            patEdit.cell = cell
            patEdit.tf_tra = tf_tra
            patEdit.seguroPat = seguroPat
            patEdit.save()

            messages.success(request, 'Paciente editado correctamente')
            return redirect('doc_patient', idPat=idPat)

        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            messages.error(request, "Ha ocurrido un error al procesar la solicitud.")
            return redirect('error_p')


#Página CREAR PACIENTE FINAL


#Página crear representantes INICIO
@login_required
@custom_login_required
def agg_rep(request,idPat):
    patbdd=Patient.objects.get(idPat=idPat)
    mombdd=MadreCita.objects.all()
    dadbdd=PadreCita.objects.all()
    return render(request,'rep/agg_rep_pat.html',{'pacientes':patbdd,'mom':mombdd, 'dad':dadbdd})

def agg_mom(request,idPat):
    if request.method == 'POST':
        nom_mom = request.POST['nom_mom']
        ape_mom = request.POST['ape_mom']
        age_mom = request.POST['age_mom']
        hij_mom = request.POST['hij_mom']
        act_mom = request.POST['act_mom']
        correo_mom = request.POST['correo_mom']
        es_cimom = request.POST['es_cimom']

        new_mom = MadreCita.objects.create(
            nom_mom=nom_mom,
            ape_mom=ape_mom,
            age_mom=age_mom,
            hij_mom = hij_mom,
            act_mom = act_mom,
            correo_mom = correo_mom,
            es_cimom = es_cimom,
        )
        messages.success(request,'Representante agregado correctamente')
        return redirect('doc_patient', idPat=idPat)

def agg_dad(request,idPat):
    if request.method == 'POST':
        nom_fat = request.POST['nom_fat']
        ape_fat = request.POST['ape_fat']
        age_fat = request.POST['age_fat']
        act_fat = request.POST['act_fat']

        new_mom = PadreCita.objects.create(
            nom_fat=nom_fat,
            ape_fat=ape_fat,
            age_fat=age_fat,
            act_fat = act_fat
        )
        messages.success(request,'Representante agregado correctamente')
        return redirect('doc_patient', idPat=idPat)


def agg_mompat(request,idPat):

    if request.method == 'POST':
     idPat = request.POST['idPat']
     id_mom = request.POST.get('id_mom')
     momSelect = MadreCita.objects.get(id=id_mom)
     patEdit = Patient.objects.get(idPat=idPat)
     patEdit.mom = momSelect
     patEdit.save()
     messages.success(request,'Mamá añadida correctamente')
     return redirect('doc_patient', idPat=idPat)


def agg_dadpat(request,idPat):

    if request.method == 'POST':
     idPat = request.POST['idPat']
     id_dad = request.POST.get('id_dad')
     dadSelect = PadreCita.objects.get(id=id_dad)
     patEdit = Patient.objects.get(idPat=idPat)
     patEdit.dad = dadSelect
     patEdit.save()
     messages.success(request,'Papá añadido correctamente')
     return redirect('doc_patient', idPat=idPat)
#Página crear representantes FINAL
