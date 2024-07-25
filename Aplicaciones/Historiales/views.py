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
from .models import Patient, Gender, MadreCita, PadreCita, Alergia, PatAler, InfoMom, observaciones, Cie10, medicina, Diagnostico, Receta
from django.views.decorators.http import require_POST
from dateutil.relativedelta import relativedelta
from num2words import num2words
from django.conf import settings
from telegram import Bot
from asgiref.sync import async_to_sync
# Create your views here.


my_token = settings.BOT_TOKEN
my_chat_id = settings.BOT_CHAT_ID

async def send_telegram_message(msg, chat_id=my_chat_id, token=my_token):
    bot_instance = Bot(token=token)
    await bot_instance.send_message(chat_id=chat_id, text=msg)

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
            async_to_sync(send_telegram_message)(f"Se ha iniciado sesión con {user.username} en Sitio administrativo Médico")
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

def pagosMama(request, idPat):
    if request.method == 'POST':
        id= request.POST['id']
        ruc_mom= request.POST['ruc_mom']
        telf_mom = request.POST['telf_mom']
        dir_mom = request.POST['dir_mom']

        pagosMom=MadreCita.objects.get(id=id)
        pagosMom.ruc_mom=ruc_mom
        pagosMom.telf_mom=telf_mom
        pagosMom.dir_mom=dir_mom
        pagosMom.save()
        messages.success(request,'Información agregada correctamente')
        return redirect('doc_patient', idPat=idPat)

    else:
        messages.error(request,'No se pudo guardar la información')
        return redirect('doc_patient', idPat=idPat)

def pagosPapa(request, idPat):
    if request.method == 'POST':
        id= request.POST['id']
        ruc_fat= request.POST['ruc_fat']
        telf_fat = request.POST['telf_fat']
        dir_fat = request.POST['dir_fat']

        pagosFat=PadreCita.objects.get(id=id)
        pagosFat.ruc_fat=ruc_fat
        pagosFat.telf_fat=telf_fat
        pagosFat.dir_fat=dir_fat
        pagosFat.save()
        messages.success(request,'Información agregada correctamente')
        return redirect('doc_patient', idPat=idPat)

    else:
        messages.error(request,'No se pudo guardar la información')
        return redirect('doc_patient', idPat=idPat)


def editPagosMama(request, idPat):
    if request.method == 'POST':
        id= request.POST['id']
        ruc_mom= request.POST['ruc_mom']
        telf_mom = request.POST['telf_mom']
        dir_mom = request.POST['dir_mom']

        pagosMom=MadreCita.objects.get(id=id)
        pagosMom.ruc_mom=ruc_mom
        pagosMom.telf_mom=telf_mom
        pagosMom.dir_mom=dir_mom
        pagosMom.save()
        messages.success(request,'Información editada correctamente')
        return redirect('doc_patient', idPat=idPat)

    else:
        messages.error(request,'No se pudo guardar la información')
        return redirect('doc_patient', idPat=idPat)

def editPagosPapa(request, idPat):
    if request.method == 'POST':
        id= request.POST['id']
        ruc_fat= request.POST['ruc_fat']
        telf_fat = request.POST['telf_fat']
        dir_fat = request.POST['dir_fat']

        pagosFat=PadreCita.objects.get(id=id)
        pagosFat.ruc_fat=ruc_fat
        pagosFat.telf_fat=telf_fat
        pagosFat.dir_fat=dir_fat
        pagosFat.save()
        messages.success(request,'Información editada correctamente')
        return redirect('doc_patient', idPat=idPat)

    else:
        messages.error(request,'No se pudo guardar la información')
        return redirect('doc_patient', idPat=idPat)


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
            birthPat = datetime.strptime(request.POST['birthPat'], '%Y-%m-%d').date()
            placePat = request.POST['placePat']
            natiPat = request.POST['natiPat']
            ciPat = request.POST['ciPat']
            id_gen = request.POST['id_gen']
            genselect = Gender.objects.get(id=id_gen)
            tf_casa = request.POST['tf_casa']
            cell = request.POST['cell']
            tf_tra = request.POST['tf_tra']
            seguroPat = 'seguroPat' in request.POST

            # Calcular la edad de la primera cita
            today = datetime.today().date()
            diff = relativedelta(today, birthPat)
            fagePat = f"{diff.years} años, {diff.months} meses y {diff.days} días"

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
                seguroPat=seguroPat,
                fagePat=fagePat  # Guardar la edad de la primera cita
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
            fagePat = request.POST['fagePat']

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
            patEdit.fagePat = fagePat
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
        diabdd = Diagnostico.objects.filter(obs=id).prefetch_related('cies')  # Obtener una lista de diagnósticos
        ciebdd = Cie10.objects.all()
        alergias = PatAler.objects.filter(paciente=patbdd).select_related('alergia')
        medbdd = medicina.objects.all()
        recbdd = Receta.objects.filter(obsmed=id)

        from num2words import num2words
        for receta in recbdd:
            receta.total_words = num2words(receta.total, lang='es')
    except observaciones.DoesNotExist:
        messages.error(request, "La observación no existe.")
        return redirect('error_p')

    return render(request, 'observation/viewobs.html', {
        'observaciones': obsbdd,
        'pacientes': patbdd,
        'diagnosticos': diabdd,  # Pasar una lista de diagnósticos
        'cies': ciebdd,
        'alergias': alergias,
        'medicinas': medbdd,
        'recetas': recbdd
    })

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

@login_required
@custom_login_required
def addDiagnostico(request, id):
    if request.method == 'POST':
        try:
            # Obtiene la observación correspondiente
            observacion = observaciones.objects.get(id=id)

            # Obtiene los datos del formulario
            cie_ids = request.POST.getlist('cie')
            tratamiento_tipo = request.POST.get('tratamiento')
            alimentacion = request.POST['alimentacion']
            examen = request.POST['examen']

            # Crea el diagnóstico
            nuevo_diagnostico = Diagnostico.objects.create(
                obs=observacion,
                tratamiento=tratamiento_tipo,
                alimentacion=alimentacion,
                examen=examen
            )

            # Añade las CIE10 al diagnóstico
            for cie_id in cie_ids:
                cie = Cie10.objects.get(id=cie_id)
                nuevo_diagnostico.cies.add(cie)

            messages.success(request, "Diagnóstico y tratamiento añadidos correctamente.")
        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            messages.error(request, "Ha ocurrido un error al procesar la solicitud.")

    return redirect('viewobs', id=id)

@login_required
@custom_login_required
def editDiagnostico(request, id):
    if request.method == 'POST':
        diagnostico_id = request.POST['id']
        alimentacion = request.POST['alimentacion']
        examen = request.POST['examen']
        tratamiento = request.POST['tratamiento']
        cie_ids = request.POST.getlist('cie')

        diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)
        diagnostico.alimentacion = alimentacion
        diagnostico.examen = examen
        diagnostico.tratamiento = tratamiento
        diagnostico.cies.set(cie_ids)

        diagnostico.save()
        messages.success(request, 'Información actualizada correctamente.')
        return redirect('viewobs', id=id)
    else:
        messages.error(request,'No se pudo editar la información')
    return redirect('viewobs', id=id)

@login_required
@custom_login_required
def addReceta(request, id):

    if request.method == 'POST':
        id = request.POST['id']
        obsmed = observaciones.objects.get(id=id)
        medicamento_id = request.POST.get('medicamentos')
        total = request.POST.get('total')
        cantidad = request.POST.get('cantidad')
        via = request.POST.get('via')
        frecuencia = request.POST.get('frecuencia')
        duracion = request.POST.get('duracion')

        receta = Receta(
            obsmed=obsmed,
            medicamento=medicina.objects.get(id=medicamento_id),
            total=total,
            cantidad=cantidad,
            via=via,
            frecuencia=frecuencia,
            duracion=duracion
        )
        receta.save()

        messages.success(request, 'Receta añadida correctamente')
        return redirect('viewobs', id=id)
    else:
        messages.error(request, 'No se pudo añadir la receta')
        return redirect('viewobs', id=id)

@login_required
@custom_login_required
def editReceta(request, idobs, idreceta):
    if request.method == 'POST':
        medicina_id = request.POST['medicamentos']
        medicinaSel = medicina.objects.get(id=medicina_id)
        total = request.POST['total']
        cantidad = request.POST['cantidad']
        via = request.POST['via']
        frecuencia = request.POST['frecuencia']
        duracion = request.POST['duracion']

        receta = get_object_or_404(Receta, id=idreceta)
        receta.medicamento = medicinaSel
        receta.total = total
        receta.cantidad = cantidad
        receta.via = via
        receta.frecuencia = frecuencia
        receta.duracion = duracion
        receta.save()
        messages.success(request, 'Receta editada correctamente')
        return redirect('viewobs', id=idobs)
    else:
        messages.error(request, 'No se pudo editar la receta')
        return redirect('viewobs', id=idobs)

@login_required
@custom_login_required
def deleteReceta (request, idReceta, idobs):
        try:
            eliminarReceta = Receta.objects.get(id=idReceta)
            eliminarReceta.delete()
            messages.success(request, 'Recetario eliminado correctamente')
        except Receta.DoesNotExist:
            messages.error(request, 'La receta no existe')
        return redirect('viewobs', id=idobs)
#PÁGINA VISTA OBSERVACIONES FINAL


#PÁGINA ALERGIAS

@login_required
@custom_login_required
def alergias(request):
    alerbdd=Alergia.objects.all()

    return render(request, 'alergy/alergies.html',{'alergias':alerbdd})

@login_required
@custom_login_required
def newalergia(request):
    if request.method == 'POST':
        nombreAlergia = request.POST['nombreAlergia']
        if Alergia.objects.filter(nombreAlergia=nombreAlergia).exists():
            messages.error(request, 'Esta alergia ya existe')
        else:
            newAler = Alergia.objects.create(nombreAlergia=nombreAlergia)
            messages.success(request, 'Alergia agregada correctamente')
        return redirect('alergias')
    else:
        messages.error(request, 'No se pudo agregar la alergia')
        return redirect('alergias')



@login_required
@custom_login_required
def deleteAlergia(request, id):
    try:
        eliminarAlergia = Alergia.objects.get(id=id)
        eliminarAlergia.delete()
        messages.success(request, 'Alergia eliminada correctamente')
    except Alergia.DoesNotExist:
        messages.error(request, 'La alergia no existe')
    return redirect('alergias')

@login_required
@custom_login_required
def editAlergia(request, id):
    if request.method == 'POST':
        id = request.POST['id']
        nombreAlergia = request.POST['nombreAlergia']

        editAlergia=Alergia.objects.get(id=id)
        editAlergia.nombreAlergia=nombreAlergia
        editAlergia.save()
        messages.success(request,'Alergia editada correctamente')
        return redirect('alergias')

    else:
        messages.error(request,'No se pudo agregar la alergia')
        return redirect('alergias')
#PÁGINA ALERGIAS


#PÁGINA CIE10 INICIO
@login_required
@custom_login_required
def reportcie(request):
    ciebdd=Cie10.objects.all()
    return render(request,'cie10/report.html', {'cies':ciebdd})

@login_required
@custom_login_required
def newcie(request):
    if request.method == 'POST':
        cod3=request.POST['cod3']
        nombrecie=request.POST['nombrecie']
        newCie=Cie10.objects.create(
            cod3=cod3,
            nombrecie=nombrecie,
        )
        messages.success(request,'Categoría agregada correctamente')
        return redirect('reportcie')
    else:
        messages.error(request,'No se pudo agregar la categoría')
        return redirect('reportcie')

@login_required
@custom_login_required
def deletecie(request, id):
    try:
        eliminarCie = Cie10.objects.get(id=id)
        eliminarCie.delete()
        messages.success(request, 'Categoría eliminada correctamente')
    except Alergia.DoesNotExist:
        messages.error(request, 'La categoría no existe')
    return redirect('reportcie')

@login_required
@custom_login_required
def editcie(request, id):
    if request.method == 'POST':
        cod3 = request.POST['cod3']
        nombrecie = request.POST['nombrecie']
        editCie = get_object_or_404(Cie10, id=id)
        editCie.cod3 = cod3
        editCie.nombrecie = nombrecie
        editCie.save()
        messages.success(request, 'Categoría editada correctamente')
        return redirect('reportcie')
    else:
        messages.error(request, 'No se pudo editar la categoría')
        return redirect('reportcie')
#PÁGINA CIE10 FINAL


#PÁGINA MEDICAMENTOS INICIO
@login_required
@custom_login_required
def medicamentos(request):
    medbdd=medicina.objects.all()
    return render(request,'medicine/medicine.html', {'medicinas':medbdd})

@login_required
@custom_login_required
def newMedicina(request):
    if request.method=='POST':
        nombregen_med=request.POST['nombregen_med']
        nombrecom_med=request.POST['nombrecom_med']
        tipo_med=request.POST['tipo_med']
        newMedicina=medicina.objects.create(
            nombregen_med=nombregen_med,
            nombrecom_med=nombrecom_med,
            tipo_med=tipo_med,
        )
        messages.success(request,'Medicamento agregado correctamente')
        return redirect('medicamentos')
    else:
        messages.error(request,'No se pudo agregar el medicamento')

@login_required
@custom_login_required
def deleteMedicina(request, id):
    try:
        eliminarMedicina = medicina.objects.get(id=id)
        eliminarMedicina.delete()
        messages.success(request, 'Medicamento eliminada correctamente')
    except Alergia.DoesNotExist:
        messages.error(request, 'El medicamento no existe')
    return redirect('medicamentos')

@login_required
@custom_login_required
def editMedicina(request, id):
    if request.method == 'POST':
        nombregen_med = request.POST['nombregen_med']
        nombrecom_med = request.POST['nombrecom_med']
        tipo_med = request.POST['tipo_med']
        editMed = get_object_or_404(medicina, id=id)
        editMed.nombregen_med = nombregen_med
        editMed.nombrecom_med = nombrecom_med
        editMed.tipo_med = tipo_med
        editMed.save()
        messages.success(request, 'Medicamento editado correctamente')
        return redirect('medicamentos')  # Cambia 'reportMedicina' a la vista a la que deseas redirigir después de la edición
    else:
        messages.error(request, 'No se pudo editar el medicamento')
        return redirect('medicamentos')
#PÁGINA MEDICAMENTOS FINAL

#PÁGINA REPRESENTANTES INICIO
@login_required
@custom_login_required
def representantesLista(request):
    patbdd=Patient.objects.all()
    mombdd=MadreCita.objects.all()
    dadbdd=PadreCita.objects.all()
    return render(request,'rep/parents.html',{'pacientes':patbdd,'mom':mombdd, 'dad':dadbdd})
#PÁGINA REPRESENTANTES FINAL
