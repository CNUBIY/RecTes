from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from datetime import datetime, timedelta, time, date
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from collections import defaultdict
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.decorators import method_decorator
from Aplicaciones.Citas.middleware import login_required as custom_login_required
from .models import Patient, Gender, MadreCita, PadreCita, Alergia, PatAler, InfoMom, observaciones
from django.views.decorators.http import require_POST
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
def doc_patient(request, idPat):
    patbdd = Patient.objects.get(idPat=idPat)
    genbdd = Gender.objects.all()
    mombdd = MadreCita.objects.all()
    dadbdd = PadreCita.objects.all()
    alerbdd = Alergia.objects.all()
    alerpatbdd = PatAler.objects.filter(paciente=idPat)

    # Utilizar filter para obtener InfoMom
    obsmom_qs = InfoMom.objects.filter(patient=idPat)
    obsmom = obsmom_qs.first() if obsmom_qs.exists() else None

    obsbdd = observaciones.objects.filter(paciente=idPat)

    return render(request, 'histo/patient.html', {
        'pacientes': patbdd,
        'generos': genbdd,
        'mom': mombdd,
        'dad': dadbdd,
        'alergias': alerbdd,
        'misalergias': alerpatbdd,
        'infomom': obsmom,
        'observaciones': obsbdd
    })


@login_required
@custom_login_required
def add_alergias(request, idPat):
    patient = Patient.objects.get(idPat=idPat)
    alergias = Alergia.objects.all()
    if request.method == 'POST':
        selected_alergias = request.POST.getlist('alergias')
        for alergia_id in selected_alergias:
            alergia = Alergia.objects.get(id=alergia_id)
            # Verificar si la alergia ya está registrada para el paciente
            if PatAler.objects.filter(paciente=patient, alergia=alergia).exists():
                messages.error(request, f'La alergia "{alergia.nombreAlergia}" ya está registrada para este paciente.')
            else:
                PatAler.objects.create(paciente=patient, alergia=alergia)
                messages.success(request, f'Alergia "{alergia.nombreAlergia}" añadida correctamente.')
        return redirect('doc_patient', idPat=idPat)  # Redirige de nuevo a la página del paciente

@login_required
@custom_login_required
def delete_alergia(request, idPat, alergia_id):
    patient = get_object_or_404(Patient, idPat=idPat)
    alergia = get_object_or_404(Alergia, id=alergia_id)
    pat_alergia = PatAler.objects.filter(paciente=patient, alergia=alergia)

    if pat_alergia.exists():
        pat_alergia.delete()
        messages.success(request, f'Alergia "{alergia.nombreAlergia}" eliminada correctamente.')
    else:
        messages.error(request, 'Alergia no encontrada para este paciente.')

    return redirect('doc_patient', idPat=idPat)


def agg_infomom(request, idPat):
    if request.method == 'POST':
        prenatal = request.POST['prenatal']
        natal = request.POST['natal']
        app = request.POST['app']
        apf = request.POST['apf']
        patient = Patient.objects.get(idPat=idPat)
        new_infomom = InfoMom.objects.create(
            prenatal=prenatal,
            natal=natal,
            app=app,
            apf=apf,
            patient=patient
        )
        messages.success(request, 'Observación agregada correctamente.')
        return redirect('doc_patient', idPat=idPat)

@login_required
@custom_login_required
def edit_infomom(request, idPat, id):
    if request.method == 'POST':
        try:
            prenatal = request.POST['prenatal']
            natal = request.POST['natal']
            app = request.POST['app']
            apf = request.POST['apf']
            infomomEdit = InfoMom.objects.get(id=id)  # Obtener la instancia correcta de InfoMom
            infomomEdit.prenatal = prenatal
            infomomEdit.natal = natal
            infomomEdit.app = app
            infomomEdit.apf = apf
            infomomEdit.save()

            messages.success(request, 'Observaciones editadas correctamente')
            return redirect('doc_patient', idPat=idPat)

        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            messages.error(request, "Ha ocurrido un error al procesar la solicitud.")
            return redirect('error_p')

@login_required
@custom_login_required
def agg_obs(request, idPat):
    if request.method == 'POST':
        #try:
            firstsect = request.POST['firstsect']
            secondsect = request.POST['secondsect']
            courtesy_visit = 'courtesyVisit' in request.POST

            # Obtener el paciente
            patient = Patient.objects.get(idPat=idPat)

            # Calcular la edad en años, meses y días
            today = date.today()
            birth_date = patient.birthPat

            years = today.year - birth_date.year
            months = today.month - birth_date.month
            days = today.day - birth_date.day

            # Ajustar los valores si es necesario
            if days < 0:
                months -= 1
                days += 30  # Esto es una simplificación; no todos los meses tienen 30 días

            if months < 0:
                years -= 1
                months += 12

            age_str = f"{years} años, {months} meses, {days} días"

            # Crear la instancia de observación con los datos del formulario
            new_observacion = observaciones.objects.create(
                paciente=patient,
                firstsect=firstsect,
                secondsect=secondsect,
                cortesia=courtesy_visit,
                new_age=age_str,
            )

            messages.success(request, 'Observación añadida correctamente')
            return redirect('doc_patient', idPat=idPat)

        # except Exception as e:
        #     print(f"Error al procesar la solicitud: {str(e)}")
        #     messages.error(request, "Ha ocurrido un error al procesar la solicitud.")
        #     return redirect('error_p')


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

@login_required
@custom_login_required
def agg_mom(request, idPat):
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
            hij_mom=hij_mom,
            act_mom=act_mom,
            correo_mom=correo_mom,
            es_cimom=es_cimom,
        )
        messages.success(request, 'Representante agregado correctamente')
        return redirect('doc_patient', idPat=idPat)

@login_required
@custom_login_required
def edit_mom (request, idPat):
    if request.method == 'POST':
        try:
            id = request.POST['id']
            nom_mom = request.POST['nom_mom']
            ape_mom = request.POST['ape_mom']
            age_mom = request.POST['age_mom']
            hij_mom = request.POST['hij_mom']
            act_mom = request.POST['act_mom']
            correo_mom = request.POST['correo_mom']
            es_cimom = request.POST['es_cimom']

            momEdit = MadreCita.objects.get(id=id)
            momEdit.nom_mom=nom_mom
            momEdit.ape_mom=ape_mom
            momEdit.age_mom=age_mom
            momEdit.hij_mom=hij_mom
            momEdit.act_mom=act_mom
            momEdit.correo_mom=correo_mom
            momEdit.es_cimom=es_cimom
            momEdit.save()
            messages.success(request, 'Mamá editada correctamente')
            return redirect('doc_patient', idPat=idPat)
        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            messages.error(request, "Ha ocurrido un error al procesar la solicitud.")
            return redirect('error_p')

@login_required
@custom_login_required
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

@login_required
@custom_login_required
def edit_dad (request, idPat):
    if request.method == 'POST':
        try:
            id = request.POST['id']
            nom_fat = request.POST['nom_fat']
            ape_fat = request.POST['ape_fat']
            age_fat = request.POST['age_fat']
            act_fat = request.POST['act_fat']
            dadEdit = PadreCita.objects.get(id=id)
            dadEdit.nom_fat=nom_fat
            dadEdit.ape_fat=ape_fat
            dadEdit.age_fat=age_fat
            dadEdit.act_fat=act_fat
            dadEdit.save()
            messages.success(request, 'Papá editado correctamente')
            return redirect('doc_patient', idPat=idPat)
        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            messages.error(request, "Ha ocurrido un error al procesar la solicitud.")
            return redirect('error_p')

@login_required
@custom_login_required
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



@login_required
@custom_login_required
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



#Página VISTA OBSERVACIONES INICIO

@login_required
@custom_login_required
def viewobs(request, id):
    try:
        obsbdd = observaciones.objects.get(id=id)
        patbdd = obsbdd.paciente  # Obtener el paciente directamente desde la observación
    except observaciones.DoesNotExist:
        messages.error(request, "La observación no existe.")
        return redirect('error_p')

    return render(request, 'observation/viewobs.html', {'observaciones': obsbdd, 'pacientes': patbdd})

@login_required
@custom_login_required
def edit_obs(request, id):
    if request.method=='POST':
        id=request.POST['id']
        firstsect=request.POST['firstsect']
        secondsect=request.POST['secondsect']
        obsEdit=observaciones.objects.get(id=id)
        obsEdit.firstsect=firstsect
        obsEdit.secondsect=secondsect
        obsEdit.save()
        messages.success(request,'Observación editada correctamente.')
        return redirect('viewobs',id=id)

#PÁGINA VISTA OBSERVACIONES FINAL
