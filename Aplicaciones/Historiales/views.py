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
from .models import Patient, Gender, MadreCita, PadreCita, Alergia, PatAler, InfoMom, observaciones, Cie10, medicina, Diagnostico, Receta, EstaturasRep, Curvas
from django.views.decorators.http import require_POST
from dateutil.relativedelta import relativedelta
from num2words import num2words
from django.conf import settings
from telegram import Bot
from asgiref.sync import async_to_sync
from decimal import Decimal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import base64
import os
from scipy.interpolate import make_interp_spline
import pandas as pd
import numpy as np
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
            if user.is_superuser or user.is_staff:
                login(request, user)
                request.session['last_activity'] = timezone.now().isoformat()  # Convertir a cadena
                async_to_sync(send_telegram_message)(f"Se ha iniciado sesión con {user.username} en Sitio administrativo Médico")
                return redirect("doc_inicio")
            else:
                messages.error(request, 'No tienes permisos para acceder a esta área.')
                return redirect('logindoc')
        else:
            messages.error(request, 'Contraseña/Correo Incorrectos')
            return redirect('logindoc')

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
def generate_growth_chart(request, idPat):
    try:
        # Ruta relativa al archivo Excel en la carpeta static
        file_path = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/tab_wfa_boys_p_0_5.xlsx')
        df = pd.read_excel(file_path, sheet_name='tab_wfa_boys_p_0_5')

        # Definir edades en meses
        ages = df['Month'].values

        # Definir percentiles
        percentile_3 = df['P3'].values
        percentile_15 = df['P15'].values
        percentile_50 = df['P50'].values
        percentile_85 = df['P85'].values
        percentile_97 = df['P97'].values

        # Filtrar los puntos del paciente con age_pat menores a 60 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__lt=60)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        spline_3 = make_interp_spline(ages, percentile_3, k=3)
        spline_15 = make_interp_spline(ages, percentile_15, k=3)
        spline_50 = make_interp_spline(ages, percentile_50, k=3)
        spline_85 = make_interp_spline(ages, percentile_85, k=3)
        spline_97 = make_interp_spline(ages, percentile_97, k=3)

        # Definir nuevas edades para la interpolación
        ages_new = np.linspace(ages.min(), ages.max(), 300)

        # Graficar los percentiles
        ax.plot(ages_new, spline_3(ages_new), 'r--', label='Percentil 3')
        ax.plot(ages_new, spline_15(ages_new), 'orange', label='Percentil 15')
        ax.plot(ages_new, spline_50(ages_new), 'g-', label='Percentil 50')
        ax.plot(ages_new, spline_85(ages_new), 'orange', label='Percentil 85')
        ax.plot(ages_new, spline_97(ages_new), 'r--', label='Percentil 97')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        pesos = [float(curva.peso) for curva in curvabdd]
        ax.plot(edades, pesos, 'o-', label='Peso del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('Peso (kg)')
        ax.set_title('Curvas de Crecimiento OMS - Peso para la Edad (0-5 años)')

        # Ajustar los ticks del eje X
        xticks = list(range(0, 61, 2))  # Ticks cada 2 meses
        xticklabels = ['Nac.', '2', '4', '6', '8', '10',
                       '1 año', '2', '4', '6', '8', '10',
                       '2 años', '2', '4', '6', '8', '10',
                       '3 años', '2', '4', '6', '8', '10',
                       '4 años', '2', '4', '6', '8', '10',
                       '5 años']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(0, 26, 2))  # Ticks cada 2 kg
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en el directorio de medios
        media_dir = settings.MEDIA_ROOT
        growth_charts_dir = os.path.join(media_dir, 'growth_charts')
        if not os.path.exists(growth_charts_dir):
            os.makedirs(growth_charts_dir)

        # Eliminar la imagen anterior si existe
        image_path = os.path.join(growth_charts_dir, f'growth_chart_{idPat}.png')
        if os.path.exists(image_path):
            os.remove(image_path)

        # Guardar la nueva imagen
        plt.savefig(image_path, format='png')
        plt.close(fig)  # Cerrar el gráfico para liberar memoria

        # Codificar la imagen en base64 para devolverla como una cadena
        with open(image_path, "rb") as image_file:
            graphic = base64.b64encode(image_file.read()).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_growth_chart: {e}")
        return None

@login_required
def generate_height_chart(request, idPat):
    try:
        # Rutas relativas a los archivos Excel en la carpeta static
        file_path_0_2 = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/boy_altura0_2.xlsx')
        file_path_2_5 = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/boy_altura2_5.xlsx')

        # Leer datos de los archivos Excel
        df_0_2 = pd.read_excel(file_path_0_2, sheet_name='tab_lhfa_boys_p_0_2')
        df_2_5 = pd.read_excel(file_path_2_5, sheet_name='tab_lhfa_boys_p_2_5')

        # Definir edades en meses
        ages_0_2 = df_0_2.index
        ages_2_5 = df_2_5.index + len(ages_0_2)

        # Concatenar los datos
        ages = list(ages_0_2) + list(ages_2_5)
        df = pd.concat([df_0_2, df_2_5])

        # Definir percentiles
        percentile_3 = list(df_0_2['P3'].values) + list(df_2_5['P3'].values)
        percentile_15 = list(df_0_2['P15'].values) + list(df_2_5['P15'].values)
        percentile_50 = list(df_0_2['P50'].values) + list(df_2_5['P50'].values)
        percentile_85 = list(df_0_2['P85'].values) + list(df_2_5['P85'].values)
        percentile_97 = list(df_0_2['P97'].values) + list(df_2_5['P97'].values)

        # Filtrar los puntos del paciente con age_pat menores a 60 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__lt=60)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        spline_3 = make_interp_spline(ages, percentile_3, k=3)
        spline_15 = make_interp_spline(ages, percentile_15, k=3)
        spline_50 = make_interp_spline(ages, percentile_50, k=3)
        spline_85 = make_interp_spline(ages, percentile_85, k=3)
        spline_97 = make_interp_spline(ages, percentile_97, k=3)

        # Definir nuevas edades para la interpolación
        ages_new = np.linspace(min(ages), max(ages), 300)

        # Graficar los percentiles
        ax.plot(ages_new, spline_3(ages_new), 'r--', label='Percentil 3')
        ax.plot(ages_new, spline_15(ages_new), 'orange', label='Percentil 15')
        ax.plot(ages_new, spline_50(ages_new), 'g-', label='Percentil 50')
        ax.plot(ages_new, spline_85(ages_new), 'orange', label='Percentil 85')
        ax.plot(ages_new, spline_97(ages_new), 'r--', label='Percentil 97')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        estaturas = [float(curva.estatura_pat) for curva in curvabdd]  # Cambiado a estatura_pat
        ax.plot(edades, estaturas, 'o-', label='Estatura del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('Estatura (cm)')
        ax.set_title('Curvas de Crecimiento OMS - Estatura para la Edad (0-5 años)')

        # Ajustar los ticks del eje X
        xticks = list(range(0, 61, 2))  # Ticks cada 2 meses hasta 60 meses (5 años)
        xticklabels = ['Nac.', '2', '4', '6', '8', '10',
                       '1 año', '2', '4', '6', '8', '10',
                       '2 años', '2', '4', '6', '8', '10',
                       '3 años', '2', '4', '6', '8', '10',
                       '4 años', '2', '4', '6', '8', '10',
                       '5 años']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(40, 121, 5))  # Ticks cada 5 cm desde 40 cm hasta 120 cm
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en el directorio de medios
        media_dir = settings.MEDIA_ROOT
        height_charts_dir = os.path.join(media_dir, 'height_charts')
        if not os.path.exists(height_charts_dir):
            os.makedirs(height_charts_dir)

        # Eliminar la imagen anterior si existe
        image_path = os.path.join(height_charts_dir, f'height_chart_{idPat}.png')
        if os.path.exists(image_path):
            os.remove(image_path)

        # Guardar la nueva imagen
        plt.savefig(image_path, format='png')
        plt.close(fig)  # Cerrar el gráfico para liberar memoria

        # Codificar la imagen en base64 para devolverla como una cadena
        with open(image_path, "rb") as image_file:
            graphic = base64.b64encode(image_file.read()).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_height_chart: {e}")
        return None

@login_required
def generate_head_circumference_chart(request, idPat):
    try:
        # Ruta relativa al archivo Excel en la carpeta static
        file_path = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/craneo_boys2_5.xlsx')
        df = pd.read_excel(file_path, sheet_name='tab_hcfa_boys_p_0_5')

        # Definir edades en meses
        ages = df['Month'].values

        # Definir percentiles
        percentile_3 = df['P3'].values
        percentile_15 = df['P15'].values
        percentile_50 = df['P50'].values
        percentile_85 = df['P85'].values
        percentile_97 = df['P97'].values

        # Filtrar los puntos del paciente con age_pat menores a 60 meses y per_enc no nulo
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__lt=60).exclude(per_enc__isnull=True)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        spline_3 = make_interp_spline(ages, percentile_3, k=3)
        spline_15 = make_interp_spline(ages, percentile_15, k=3)
        spline_50 = make_interp_spline(ages, percentile_50, k=3)
        spline_85 = make_interp_spline(ages, percentile_85, k=3)
        spline_97 = make_interp_spline(ages, percentile_97, k=3)

        # Definir nuevas edades para la interpolación
        ages_new = np.linspace(ages.min(), ages.max(), 300)

        # Graficar los percentiles
        ax.plot(ages_new, spline_3(ages_new), 'r--', label='Percentil 3')
        ax.plot(ages_new, spline_15(ages_new), 'orange', label='Percentil 15')
        ax.plot(ages_new, spline_50(ages_new), 'g-', label='Percentil 50')
        ax.plot(ages_new, spline_85(ages_new), 'orange', label='Percentil 85')
        ax.plot(ages_new, spline_97(ages_new), 'r--', label='Percentil 97')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        perimetros = [float(curva.per_enc) for curva in curvabdd if curva.per_enc is not None]
        ax.plot(edades, perimetros, 'o-', label='Perímetro cefálico del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('Perímetro Cefálico (cm)')
        ax.set_title('Curvas de Crecimiento OMS - Perímetro Cefálico para la Edad (0-5 años)')

        # Ajustar los ticks del eje X
        xticks = list(range(0, 61, 2))  # Ticks cada 2 meses hasta 60 meses (5 años)
        xticklabels = ['Nac.', '2', '4', '6', '8', '10',
                       '1 año', '2', '4', '6', '8', '10',
                       '2 años', '2', '4', '6', '8', '10',
                       '3 años', '2', '4', '6', '8', '10',
                       '4 años', '2', '4', '6', '8', '10',
                       '5 años']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(32, 55, 2))  # Ticks cada 2 cm desde 32 cm hasta 54 cm
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en el directorio de medios
        media_dir = settings.MEDIA_ROOT
        head_circumference_charts_dir = os.path.join(media_dir, 'head_circumference_charts')
        if not os.path.exists(head_circumference_charts_dir):
            os.makedirs(head_circumference_charts_dir)

        # Eliminar la imagen anterior si existe
        image_path = os.path.join(head_circumference_charts_dir, f'head_circumference_chart_{idPat}.png')
        if os.path.exists(image_path):
            os.remove(image_path)

        # Guardar la nueva imagen
        plt.savefig(image_path, format='png')
        plt.close(fig)  # Cerrar el gráfico para liberar memoria

        # Codificar la imagen en base64 para devolverla como una cadena
        with open(image_path, "rb") as image_file:
            graphic = base64.b64encode(image_file.read()).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_head_circumference_chart: {e}")
        return None

@login_required
def generate_bmi_chart(request, idPat):
    try:
        # Rutas relativas a los archivos Excel en la carpeta static
        file_path_0_2 = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/imc_boy0_2.xlsx')
        file_path_2_5 = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/imc_boy2_5.xlsx')

        # Leer datos de los archivos Excel
        df_0_2 = pd.read_excel(file_path_0_2, sheet_name='tab_bmi_boys_p_0_2')  # Ajusta el nombre de la hoja según corresponda
        df_2_5 = pd.read_excel(file_path_2_5, sheet_name='tab_bmi_boys_p_2_5')  # Ajusta el nombre de la hoja según corresponda

        # Definir edades en meses
        ages_0_2 = df_0_2.index
        ages_2_5 = df_2_5.index + len(ages_0_2)

        # Concatenar los datos
        ages = list(ages_0_2) + list(ages_2_5)
        df = pd.concat([df_0_2, df_2_5])

        # Definir percentiles
        percentile_3 = list(df_0_2['P3'].values) + list(df_2_5['P3'].values)
        percentile_15 = list(df_0_2['P15'].values) + list(df_2_5['P15'].values)
        percentile_50 = list(df_0_2['P50'].values) + list(df_2_5['P50'].values)
        percentile_85 = list(df_0_2['P85'].values) + list(df_2_5['P85'].values)
        percentile_97 = list(df_0_2['P97'].values) + list(df_2_5['P97'].values)

        # Filtrar los puntos del paciente con age_pat menores a 60 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__lt=60)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        spline_3 = make_interp_spline(ages, percentile_3, k=3)
        spline_15 = make_interp_spline(ages, percentile_15, k=3)
        spline_50 = make_interp_spline(ages, percentile_50, k=3)
        spline_85 = make_interp_spline(ages, percentile_85, k=3)
        spline_97 = make_interp_spline(ages, percentile_97, k=3)

        # Definir nuevas edades para la interpolación
        ages_new = np.linspace(min(ages), max(ages), 300)

        # Graficar los percentiles
        ax.plot(ages_new, spline_3(ages_new), 'r--', label='Percentil 3')
        ax.plot(ages_new, spline_15(ages_new), 'orange', label='Percentil 15')
        ax.plot(ages_new, spline_50(ages_new), 'g-', label='Percentil 50')
        ax.plot(ages_new, spline_85(ages_new), 'orange', label='Percentil 85')
        ax.plot(ages_new, spline_97(ages_new), 'r--', label='Percentil 97')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        imcs = [float(curva.IMC) for curva in curvabdd]
        ax.plot(edades, imcs, 'o-', label='IMC del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('IMC (kg/m²)')
        ax.set_title('Curvas de Crecimiento OMS - IMC para la Edad (0-5 años)')

        # Ajustar los ticks del eje X
        xticks = list(range(0, 61, 2))  # Ticks cada 2 meses hasta 60 meses (5 años)
        xticklabels = ['Nac.', '2', '4', '6', '8', '10',
                       '1 año', '2', '4', '6', '8', '10',
                       '2 años', '2', '4', '6', '8', '10',
                       '3 años', '2', '4', '6', '8', '10',
                       '4 años', '2', '4', '6', '8', '10',
                       '5 años']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(10, 21, 1))  # Ticks cada 1 kg/m² desde 10 kg/m² hasta 20 kg/m²
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en el directorio de medios
        media_dir = settings.MEDIA_ROOT
        bmi_charts_dir = os.path.join(media_dir, 'bmi_charts')
        if not os.path.exists(bmi_charts_dir):
            os.makedirs(bmi_charts_dir)

        # Eliminar la imagen anterior si existe
        image_path = os.path.join(bmi_charts_dir, f'bmi_chart_{idPat}.png')
        if os.path.exists(image_path):
            os.remove(image_path)

        # Guardar la nueva imagen
        plt.savefig(image_path, format='png')
        plt.close(fig)  # Cerrar el gráfico para liberar memoria

        # Codificar la imagen en base64 para devolverla como una cadena
        with open(image_path, "rb") as image_file:
            graphic = base64.b64encode(image_file.read()).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_bmi_chart: {e}")
        return None


@login_required
def generate_growth_chart_girls(request, idPat):
    try:
        # Ruta relativa al archivo Excel en la carpeta static
        file_path = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/peso_girl0_5.xlsx')
        df = pd.read_excel(file_path, sheet_name='tab_wfa_girls_p_0_5')  # Ajusta el nombre de la hoja según corresponda

        # Definir edades en meses
        ages = df['Month'].values

        # Definir percentiles
        percentile_3 = df['P3'].values
        percentile_15 = df['P15'].values
        percentile_50 = df['P50'].values
        percentile_85 = df['P85'].values
        percentile_97 = df['P97'].values

        # Filtrar los puntos del paciente con age_pat menores a 60 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__lt=60)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        spline_3 = make_interp_spline(ages, percentile_3, k=3)
        spline_15 = make_interp_spline(ages, percentile_15, k=3)
        spline_50 = make_interp_spline(ages, percentile_50, k=3)
        spline_85 = make_interp_spline(ages, percentile_85, k=3)
        spline_97 = make_interp_spline(ages, percentile_97, k=3)

        # Definir nuevas edades para la interpolación
        ages_new = np.linspace(ages.min(), ages.max(), 300)

        # Graficar los percentiles
        ax.plot(ages_new, spline_3(ages_new), 'r--', label='Percentil 3')
        ax.plot(ages_new, spline_15(ages_new), 'orange', label='Percentil 15')
        ax.plot(ages_new, spline_50(ages_new), 'g-', label='Percentil 50')
        ax.plot(ages_new, spline_85(ages_new), 'orange', label='Percentil 85')
        ax.plot(ages_new, spline_97(ages_new), 'r--', label='Percentil 97')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        pesos = [float(curva.peso) for curva in curvabdd]
        ax.plot(edades, pesos, 'o-', label='Peso del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('Peso (kg)')
        ax.set_title('Curvas de Crecimiento OMS - Peso para la Edad (0-5 años) - Niñas')

        # Ajustar los ticks del eje X
        xticks = list(range(0, 61, 2))  # Ticks cada 2 meses
        xticklabels = ['Nac.', '2', '4', '6', '8', '10',
                       '1 año', '2', '4', '6', '8', '10',
                       '2 años', '2', '4', '6', '8', '10',
                       '3 años', '2', '4', '6', '8', '10',
                       '4 años', '2', '4', '6', '8', '10',
                       '5 años']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(0, 26, 2))  # Ticks cada 2 kg
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en el directorio de medios
        media_dir = settings.MEDIA_ROOT
        growth_charts_dir = os.path.join(media_dir, 'growth_charts_girls')
        if not os.path.exists(growth_charts_dir):
            os.makedirs(growth_charts_dir)

        # Eliminar la imagen anterior si existe
        image_path = os.path.join(growth_charts_dir, f'growth_chart_girls_{idPat}.png')
        if os.path.exists(image_path):
            os.remove(image_path)

        # Guardar la nueva imagen
        plt.savefig(image_path, format='png')
        plt.close(fig)  # Cerrar el gráfico para liberar memoria

        # Codificar la imagen en base64 para devolverla como una cadena
        with open(image_path, "rb") as image_file:
            graphic = base64.b64encode(image_file.read()).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_growth_chart_girls: {e}")
        return None

@login_required
def generate_height_chart_girls(request, idPat):
    try:
        # Rutas relativas a los archivos Excel en la carpeta static
        file_path_0_2 = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/girl_altura0_2.xlsx')
        file_path_2_5 = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/girl_altura2_5.xlsx')

        # Leer datos de los archivos Excel
        df_0_2 = pd.read_excel(file_path_0_2, sheet_name='tab_lhfa_girls_p_0_2')  # Ajusta el nombre de la hoja según corresponda
        df_2_5 = pd.read_excel(file_path_2_5, sheet_name='tab_lhfa_girls_p_2_5')  # Ajusta el nombre de la hoja según corresponda

        # Definir edades en meses
        ages_0_2 = df_0_2.index
        ages_2_5 = df_2_5.index + len(ages_0_2)

        # Concatenar los datos
        ages = list(ages_0_2) + list(ages_2_5)
        df = pd.concat([df_0_2, df_2_5])

        # Definir percentiles
        percentile_3 = list(df_0_2['P3'].values) + list(df_2_5['P3'].values)
        percentile_15 = list(df_0_2['P15'].values) + list(df_2_5['P15'].values)
        percentile_50 = list(df_0_2['P50'].values) + list(df_2_5['P50'].values)
        percentile_85 = list(df_0_2['P85'].values) + list(df_2_5['P85'].values)
        percentile_97 = list(df_0_2['P97'].values) + list(df_2_5['P97'].values)

        # Filtrar los puntos del paciente con age_pat menores a 60 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__lt=60)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        spline_3 = make_interp_spline(ages, percentile_3, k=3)
        spline_15 = make_interp_spline(ages, percentile_15, k=3)
        spline_50 = make_interp_spline(ages, percentile_50, k=3)
        spline_85 = make_interp_spline(ages, percentile_85, k=3)
        spline_97 = make_interp_spline(ages, percentile_97, k=3)

        # Definir nuevas edades para la interpolación
        ages_new = np.linspace(min(ages), max(ages), 300)

        # Graficar los percentiles
        ax.plot(ages_new, spline_3(ages_new), 'r--', label='Percentil 3')
        ax.plot(ages_new, spline_15(ages_new), 'orange', label='Percentil 15')
        ax.plot(ages_new, spline_50(ages_new), 'g-', label='Percentil 50')
        ax.plot(ages_new, spline_85(ages_new), 'orange', label='Percentil 85')
        ax.plot(ages_new, spline_97(ages_new), 'r--', label='Percentil 97')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        estaturas = [float(curva.estatura_pat) for curva in curvabdd]
        ax.plot(edades, estaturas, 'o-', label='Estatura del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('Estatura (cm)')
        ax.set_title('Curvas de Crecimiento OMS - Estatura para la Edad (0-5 años) - Niñas')

        # Ajustar los ticks del eje X
        xticks = list(range(0, 61, 2))  # Ticks cada 2 meses hasta 60 meses (5 años)
        xticklabels = ['Nac.', '2', '4', '6', '8', '10',
                       '1 año', '2', '4', '6', '8', '10',
                       '2 años', '2', '4', '6', '8', '10',
                       '3 años', '2', '4', '6', '8', '10',
                       '4 años', '2', '4', '6', '8', '10',
                       '5 años']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(40, 121, 5))  # Ticks cada 5 cm desde 40 cm hasta 120 cm
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        height_chart_girls = base64.b64encode(image_png).decode('utf-8')

        return height_chart_girls

    except Exception as e:
        print(f"Error en generate_height_chart_girls: {e}")
        return None

@login_required
def generate_head_circumference_chart_girls(request, idPat):
    try:
        # Ruta relativa al archivo Excel en la carpeta static
        file_path = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/craneo_girls0_5.xlsx')
        df = pd.read_excel(file_path, sheet_name='tab_hcfa_girls_p_0_5')  # Ajusta el nombre de la hoja si es necesario

        # Definir edades en meses
        ages = df['Month'].values

        # Definir percentiles
        percentile_3 = df['P3'].values
        percentile_15 = df['P15'].values
        percentile_50 = df['P50'].values
        percentile_85 = df['P85'].values
        percentile_97 = df['P97'].values

        # Filtrar los puntos del paciente con age_pat menores a 60 meses y per_enc no nulos
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__lt=60, per_enc__isnull=False)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        spline_3 = make_interp_spline(ages, percentile_3, k=3)
        spline_15 = make_interp_spline(ages, percentile_15, k=3)
        spline_50 = make_interp_spline(ages, percentile_50, k=3)
        spline_85 = make_interp_spline(ages, percentile_85, k=3)
        spline_97 = make_interp_spline(ages, percentile_97, k=3)

        # Definir nuevas edades para la interpolación
        ages_new = np.linspace(ages.min(), ages.max(), 300)

        # Graficar los percentiles
        ax.plot(ages_new, spline_3(ages_new), 'r--', label='Percentil 3')
        ax.plot(ages_new, spline_15(ages_new), 'orange', label='Percentil 15')
        ax.plot(ages_new, spline_50(ages_new), 'g-', label='Percentil 50')
        ax.plot(ages_new, spline_85(ages_new), 'orange', label='Percentil 85')
        ax.plot(ages_new, spline_97(ages_new), 'r--', label='Percentil 97')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        perimetros = [float(curva.per_enc) for curva in curvabdd]
        ax.plot(edades, perimetros, 'o-', label='Perímetro cefálico del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('Perímetro Cefálico (cm)')
        ax.set_title('Curvas de Crecimiento OMS - Perímetro Cefálico para la Edad (0-5 años) - Niñas')

        # Ajustar los ticks del eje X
        xticks = list(range(0, 61, 2))  # Ticks cada 2 meses hasta 60 meses (5 años)
        xticklabels = ['Nac.', '2', '4', '6', '8', '10',
                       '1 año', '2', '4', '6', '8', '10',
                       '2 años', '2', '4', '6', '8', '10',
                       '3 años', '2', '4', '6', '8', '10',
                       '4 años', '2', '4', '6', '8', '10',
                       '5 años']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(32, 55, 2))  # Ticks cada 2 cm desde 32 cm hasta 54 cm
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        head_circumference_chart_girls = base64.b64encode(image_png).decode('utf-8')

        return head_circumference_chart_girls

    except Exception as e:
        print(f"Error en generate_head_circumference_chart_girls: {e}")
        return None

@login_required
def generate_bmi_chart_girls(request, idPat):
    try:
        # Rutas relativas a los archivos Excel en la carpeta static
        file_path_0_2 = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/imc_girl0_2.xlsx')
        file_path_2_5 = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/imc_girl2_5.xlsx')

        # Leer datos de los archivos Excel
        df_0_2 = pd.read_excel(file_path_0_2, sheet_name='tab_bmi_girls_p_0_2')  # Ajusta el nombre de la hoja según corresponda
        df_2_5 = pd.read_excel(file_path_2_5, sheet_name='tab_bmi_girls_p_2_5')  # Ajusta el nombre de la hoja según corresponda

        # Definir edades en meses
        ages_0_2 = df_0_2.index
        ages_2_5 = df_2_5.index + len(ages_0_2)

        # Concatenar los datos
        ages = list(ages_0_2) + list(ages_2_5)
        df = pd.concat([df_0_2, df_2_5])

        # Definir percentiles
        percentile_3 = list(df_0_2['P3'].values) + list(df_2_5['P3'].values)
        percentile_15 = list(df_0_2['P15'].values) + list(df_2_5['P15'].values)
        percentile_50 = list(df_0_2['P50'].values) + list(df_2_5['P50'].values)
        percentile_85 = list(df_0_2['P85'].values) + list(df_2_5['P85'].values)
        percentile_97 = list(df_0_2['P97'].values) + list(df_2_5['P97'].values)

        # Filtrar los puntos del paciente con age_pat menores a 60 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__lt=60)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        spline_3 = make_interp_spline(ages, percentile_3, k=3)
        spline_15 = make_interp_spline(ages, percentile_15, k=3)
        spline_50 = make_interp_spline(ages, percentile_50, k=3)
        spline_85 = make_interp_spline(ages, percentile_85, k=3)
        spline_97 = make_interp_spline(ages, percentile_97, k=3)

        # Definir nuevas edades para la interpolación
        ages_new = np.linspace(min(ages), max(ages), 300)

        # Graficar los percentiles
        ax.plot(ages_new, spline_3(ages_new), 'r--', label='Percentil 3')
        ax.plot(ages_new, spline_15(ages_new), 'orange', label='Percentil 15')
        ax.plot(ages_new, spline_50(ages_new), 'g-', label='Percentil 50')
        ax.plot(ages_new, spline_85(ages_new), 'orange', label='Percentil 85')
        ax.plot(ages_new, spline_97(ages_new), 'r--', label='Percentil 97')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        imcs = [float(curva.IMC) for curva in curvabdd]
        ax.plot(edades, imcs, 'o-', label='IMC del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('IMC (kg/m²)')
        ax.set_title('Curvas de Crecimiento OMS - IMC para la Edad (0-5 años) - Niñas')

        # Ajustar los ticks del eje X
        xticks = list(range(0, 61, 2))  # Ticks cada 2 meses hasta 60 meses (5 años)
        xticklabels = ['Nac.', '2', '4', '6', '8', '10',
                       '1 año', '2', '4', '6', '8', '10',
                       '2 años', '2', '4', '6', '8', '10',
                       '3 años', '2', '4', '6', '8', '10',
                       '4 años', '2', '4', '6', '8', '10',
                       '5 años']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(10, 21, 1))  # Ticks cada 1 kg/m² desde 10 kg/m² hasta 21 kg/m²
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        bmi_chart_girls = base64.b64encode(image_png).decode('utf-8')

        return bmi_chart_girls

    except Exception as e:
        print(f"Error en generate_bmi_chart_girls: {e}")
        return None

@login_required
def generate_growth_chart_2_to_20(request, idPat):
    try:
        # Ruta relativa al archivo Excel en la carpeta static
        file_path = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/wtageboys.xlsx')
        df = pd.read_excel(file_path, sheet_name='wtage')

        # Filtrar los datos para edades de 24 meses (2 años) a 240 meses (20 años)
        df = df[(df['Agemos'] >= 24) & (df['Agemos'] <= 240)]

        # Definir edades en meses
        ages = df['Agemos'].values

        # Definir percentiles con colores
        percentiles = {
            'P5': ('r-', df['P5'].values),
            'P10': ('orange', df['P10'].values),
            'P25': ('yellow', df['P25'].values),
            'P50': ('g-', df['P50'].values),
            'P75': ('yellow', df['P75'].values),
            'P90': ('orange', df['P90'].values),
            'P95': ('r-', df['P95'].values)
        }

        # Filtrar los puntos del paciente con age_pat entre 24 y 240 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__gte=24, age_pat__lte=240)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        for label, (color, values) in percentiles.items():
            spline = make_interp_spline(ages, values, k=3)
            ages_new = np.linspace(ages.min(), ages.max(), 300)
            ax.plot(ages_new, spline(ages_new), color, label=f'Percentil {label}')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        pesos = [float(curva.peso) for curva in curvabdd]
        ax.plot(edades, pesos, 'o-', label='Peso del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('Peso (kg)')
        ax.set_title('Curvas de Crecimiento - Peso para la Edad (2-20 años)')

        # Ajustar los ticks del eje X
        xticks = list(range(24, 241, 12))  # Ticks cada año
        xticklabels = [f'{i//12} años' for i in xticks]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(0, 101, 5))  # Ticks cada 5 kg
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_growth_chart_2_to_20: {e}")
        return None

@login_required
def generate_height_chart_2_to_20(request, idPat):
    try:
        # Ruta relativa al archivo Excel en la carpeta static
        file_path = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/statageboys.xlsx')
        df = pd.read_excel(file_path, sheet_name='statage')

        # Filtrar los datos para edades de 24 meses (2 años) a 240 meses (20 años)
        df = df[(df['Agemos'] >= 24) & (df['Agemos'] <= 240)]

        # Definir edades en meses
        ages = df['Agemos'].values

        # Definir percentiles con colores
        percentiles = {
            'P5': ('r-', df['P5'].values),
            'P10': ('orange', df['P10'].values),
            'P25': ('yellow', df['P25'].values),
            'P50': ('g-', df['P50'].values),
            'P75': ('yellow', df['P75'].values),
            'P90': ('orange', df['P90'].values),
            'P95': ('r-', df['P95'].values)
        }

        # Filtrar los puntos del paciente con age_pat entre 24 y 240 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__gte=24, age_pat__lte=240)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        for label, (color, values) in percentiles.items():
            spline = make_interp_spline(ages, values, k=3)
            ages_new = np.linspace(ages.min(), ages.max(), 300)
            ax.plot(ages_new, spline(ages_new), color, label=f'Percentil {label}')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        estaturas = [float(curva.estatura_pat) for curva in curvabdd]
        ax.plot(edades, estaturas, 'o-', label='Altura del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('Altura (cm)')
        ax.set_title('Curvas de Crecimiento - Altura para la Edad (2-20 años)')

        # Ajustar los ticks del eje X
        xticks = list(range(24, 241, 12))  # Ticks cada año
        xticklabels = [f'{i//12} años' for i in xticks]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(60, 201, 10))  # Ticks cada 10 cm
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_height_chart_2_to_20: {e}")
        return None

@login_required
def generate_bmi_chart_2_to_20(request, idPat):
    try:
        # Ruta relativa al archivo Excel en la carpeta static
        file_path = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/bmiagerevboys.xlsx')
        df = pd.read_excel(file_path, sheet_name='bmiage')

        # Filtrar los datos para edades de 24 meses (2 años) a 240 meses (20 años)
        df = df[(df['Agemos'] >= 24) & (df['Agemos'] <= 240)]

        # Definir edades en meses
        ages = df['Agemos'].values

        # Definir percentiles con colores
        percentiles = {
            'P5': ('r-', df['P5'].values),
            'P10': ('orange', df['P10'].values),
            'P25': ('yellow', df['P25'].values),
            'P50': ('g-', df['P50'].values),
            'P75': ('yellow', df['P75'].values),
            'P90': ('orange', df['P90'].values),
            'P95': ('r-', df['P95'].values)
        }

        # Filtrar los puntos del paciente con age_pat entre 24 y 240 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__gte=24, age_pat__lte=240)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        for label, (color, values) in percentiles.items():
            spline = make_interp_spline(ages, values, k=3)
            ages_new = np.linspace(ages.min(), ages.max(), 300)
            ax.plot(ages_new, spline(ages_new), color, label=f'Percentil {label}')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        imcs = [float(curva.IMC) for curva in curvabdd]
        ax.plot(edades, imcs, 'o-', label='IMC del paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('IMC')
        ax.set_title('Curvas de Crecimiento - IMC para la Edad (2-20 años)')

        # Ajustar los ticks del eje X
        xticks = list(range(24, 241, 12))  # Ticks cada año
        xticklabels = [f'{i//12} años' for i in xticks]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(10, 40, 2))  # Ticks cada 2 unidades de IMC
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_bmi_chart_2_to_20: {e}")
        return None

@login_required
def generate_growth_chart_girls_2_to_20(request, idPat):
    try:
        # Ruta relativa al archivo Excel en la carpeta static
        file_path = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/wtagegirls.xlsx')
        df = pd.read_excel(file_path, sheet_name='wtage')

        # Filtrar los datos para edades de 24 meses (2 años) a 240 meses (20 años)
        df = df[(df['Agemos'] >= 24) & (df['Agemos'] <= 240)]

        # Definir edades en meses
        ages = df['Agemos'].values

        # Definir percentiles con colores
        percentiles = {
            'P5': ('r-', df['P5'].values),
            'P10': ('orange', df['P10'].values),
            'P25': ('yellow', df['P25'].values),
            'P50': ('g-', df['P50'].values),
            'P75': ('yellow', df['P75'].values),
            'P90': ('orange', df['P90'].values),
            'P95': ('r-', df['P95'].values)
        }

        # Filtrar los puntos del paciente con age_pat entre 24 y 240 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__gte=24, age_pat__lte=240)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        for label, (color, values) in percentiles.items():
            spline = make_interp_spline(ages, values, k=3)
            ages_new = np.linspace(ages.min(), ages.max(), 300)
            ax.plot(ages_new, spline(ages_new), color, label=f'Percentil {label}')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        pesos = [float(curva.peso) for curva in curvabdd]
        ax.plot(edades, pesos, 'o-', label='Peso de la paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('Peso (kg)')
        ax.set_title('Curvas de Crecimiento - Peso para la Edad (2-20 años) - Niñas')

        # Ajustar los ticks del eje X
        xticks = list(range(24, 241, 12))  # Ticks cada año
        xticklabels = [f'{i//12} años' for i in xticks]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(5, 105, 5))  # Ticks cada 5 kg
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_growth_chart_girls_2_to_20: {e}")
        return None

@login_required
def generate_height_chart_girls_2_to_20(request, idPat):
    try:
        # Ruta relativa al archivo Excel en la carpeta static
        file_path = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/statagegirls.xlsx')
        df = pd.read_excel(file_path, sheet_name='statage')

        # Filtrar los datos para edades de 24 meses (2 años) a 240 meses (20 años)
        df = df[(df['Agemos'] >= 24) & (df['Agemos'] <= 240)]

        # Definir edades en meses
        ages = df['Agemos'].values

        # Definir percentiles con colores
        percentiles = {
            'P5': ('r-', df['P5'].values),
            'P10': ('orange', df['P10'].values),
            'P25': ('yellow', df['P25'].values),
            'P50': ('g-', df['P50'].values),
            'P75': ('yellow', df['P75'].values),
            'P90': ('orange', df['P90'].values),
            'P95': ('r-', df['P95'].values)
        }

        # Filtrar los puntos del paciente con age_pat entre 24 y 240 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__gte=24, age_pat__lte=240)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        for label, (color, values) in percentiles.items():
            spline = make_interp_spline(ages, values, k=3)
            ages_new = np.linspace(ages.min(), ages.max(), 300)
            ax.plot(ages_new, spline(ages_new), color, label=f'Percentil {label}')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        estaturas = [float(curva.estatura_pat) for curva in curvabdd]
        ax.plot(edades, estaturas, 'o-', label='Altura de la paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('Altura (cm)')
        ax.set_title('Curvas de Crecimiento - Altura para la Edad (2-20 años) - Niñas')

        # Ajustar los ticks del eje X
        xticks = list(range(24, 241, 12))  # Ticks cada año
        xticklabels = [f'{i//12} años' for i in xticks]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(60, 201, 10))  # Ticks cada 10 cm
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_height_chart_girls_2_to_20: {e}")
        return None


@login_required
def generate_bmi_chart_girls_2_to_20(request, idPat):
    try:
        # Ruta relativa al archivo Excel en la carpeta static
        file_path = os.path.join(settings.BASE_DIR, 'Tesis/static/curvas/bmiagerevgirls.xlsx')
        df = pd.read_excel(file_path, sheet_name='bmiage')

        # Filtrar los datos para edades de 24 meses (2 años) a 240 meses (20 años)
        df = df[(df['Agemos'] >= 24) & (df['Agemos'] <= 240)]

        # Definir edades en meses
        ages = df['Agemos'].values

        # Definir percentiles con colores
        percentiles = {
            'P5': ('r-', df['P5'].values),
            'P10': ('orange', df['P10'].values),
            'P25': ('yellow', df['P25'].values),
            'P50': ('g-', df['P50'].values),
            'P75': ('yellow', df['P75'].values),
            'P90': ('orange', df['P90'].values),
            'P95': ('r-', df['P95'].values)
        }

        # Filtrar los puntos del paciente con age_pat entre 24 y 240 meses
        curvabdd = Curvas.objects.filter(paciente=idPat, age_pat__gte=24, age_pat__lte=240)

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear splines para suavizar las curvas
        for label, (color, values) in percentiles.items():
            spline = make_interp_spline(ages, values, k=3)
            ages_new = np.linspace(ages.min(), ages.max(), 300)
            ax.plot(ages_new, spline(ages_new), color, label=f'Percentil {label}')

        # Graficar los datos del paciente
        edades = [float(curva.age_pat) for curva in curvabdd]
        imcs = [float(curva.IMC) for curva in curvabdd]
        ax.plot(edades, imcs, 'o-', label='IMC de la paciente')

        # Configurar etiquetas y título
        ax.set_xlabel('Edad (meses)')
        ax.set_ylabel('IMC')
        ax.set_title('Curvas de Crecimiento - IMC para la Edad (2-20 años) - Niñas')

        # Ajustar los ticks del eje X
        xticks = list(range(24, 241, 12))  # Ticks cada año
        xticklabels = [f'{i//12} años' for i in xticks]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha='right')

        # Ajustar los ticks del eje Y
        yticks = list(range(10, 40, 2))  # Ticks cada 2 unidades de IMC
        ax.set_yticks(yticks)

        # Añadir la cuadrícula
        ax.grid(True)

        # Agregar leyenda
        ax.legend()

        # Guardar gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')

        return graphic

    except Exception as e:
        print(f"Error en generate_bmi_chart_girls_2_to_20: {e}")
        return None


@login_required
def doc_patient(request, idPat):
    patbdd = Patient.objects.get(idPat=idPat)
    genbdd = Gender.objects.all()
    mombdd = MadreCita.objects.all()
    dadbdd = PadreCita.objects.all()
    alerbdd = Alergia.objects.all()
    alerpatbdd = PatAler.objects.filter(paciente=idPat)
    estrepbdd = EstaturasRep.objects.filter(paciente=idPat).first()
    curvabdd = Curvas.objects.filter(paciente=idPat)

    # Convertir comas a puntos en estaturas
    if estrepbdd:
        estrepbdd.estatura_mom = str(estrepbdd.estatura_mom).replace(',', '.')
        estrepbdd.estatura_dad = str(estrepbdd.estatura_dad).replace(',', '.')

    # Utilizar filter para obtener InfoMom
    obsmom_qs = InfoMom.objects.filter(patient=idPat)
    obsmom = obsmom_qs.first() if obsmom_qs.exists() else None

    obsbdd = observaciones.objects.filter(paciente=idPat)

    # Generar gráficos según el género del paciente
    if patbdd.genPat.nombreGen == 'Masculino':
        weight_chart = generate_growth_chart(request, idPat)
        height_chart = generate_height_chart(request, idPat)
        head_circumference_chart = generate_head_circumference_chart(request, idPat)
        bmi_chart = generate_bmi_chart(request, idPat)
        weight_chart_girls = None
        height_chart_girls = None
        head_circumference_chart_girls = None
        bmi_chart_girls = None
        growth_chart_2_to_20 = generate_growth_chart_2_to_20(request, idPat)
        height_chart_2_to_20 = generate_height_chart_2_to_20(request, idPat)
        bmi_chart_2_to_20 = generate_bmi_chart_2_to_20(request, idPat)
        growth_chart_girls_2_to_20 = None
        height_chart_girls_2_to_20 = None
        bmi_chart_girls_2_to_20 = None
    elif patbdd.genPat.nombreGen == 'Femenino':
        weight_chart = None
        height_chart = None
        head_circumference_chart = None
        bmi_chart = None
        weight_chart_girls = generate_growth_chart_girls(request, idPat)
        height_chart_girls = generate_height_chart_girls(request, idPat)
        head_circumference_chart_girls = generate_head_circumference_chart_girls(request, idPat)
        bmi_chart_girls = generate_bmi_chart_girls(request, idPat)
        growth_chart_2_to_20 = None
        height_chart_2_to_20 = None
        bmi_chart_2_to_20 = None
        growth_chart_girls_2_to_20 = generate_growth_chart_girls_2_to_20(request, idPat)
        height_chart_girls_2_to_20 = generate_height_chart_girls_2_to_20(request, idPat)
        bmi_chart_girls_2_to_20 = generate_bmi_chart_girls_2_to_20(request, idPat)
    else:
        weight_chart = None
        height_chart = None
        head_circumference_chart = None
        bmi_chart = None
        weight_chart_girls = None
        height_chart_girls = None
        head_circumference_chart_girls = None
        bmi_chart_girls = None
        growth_chart_2_to_20 = None
        height_chart_2_to_20 = None
        bmi_chart_2_to_20 = None
        growth_chart_girls_2_to_20 = None
        height_chart_girls_2_to_20 = None
        bmi_chart_girls_2_to_20 = None

    return render(request, 'histo/patient.html', {
        'pacientes': patbdd,
        'generos': genbdd,
        'mom': mombdd,
        'dad': dadbdd,
        'alergias': alerbdd,
        'misalergias': alerpatbdd,
        'infomom': obsmom,
        'observaciones': obsbdd,
        'estaturas': estrepbdd,
        'curvas': curvabdd,
        'weight_chart': weight_chart if weight_chart else "No se pudo generar la gráfica de peso para la edad.",
        'height_chart': height_chart if height_chart else "No se pudo generar la gráfica de altura para la edad.",
        'head_circumference_chart': head_circumference_chart if head_circumference_chart else "No se pudo generar la gráfica de perímetro cefálico para la edad.",
        'bmi_chart': bmi_chart if bmi_chart else "No se pudo generar la gráfica de IMC para la edad.",
        'weight_chart_girls': weight_chart_girls if weight_chart_girls else "No se pudo generar la gráfica de peso para la edad (niñas).",
        'height_chart_girls': height_chart_girls if height_chart_girls else "No se pudo generar la gráfica de altura para la edad (niñas).",
        'head_circumference_chart_girls': head_circumference_chart_girls if head_circumference_chart_girls else "No se pudo generar la gráfica de perímetro cefálico para la edad (niñas).",
        'bmi_chart_girls': bmi_chart_girls if bmi_chart_girls else "No se pudo generar la gráfica de IMC para la edad (niñas).",
        'growth_chart_2_to_20': growth_chart_2_to_20 if growth_chart_2_to_20 else "No se pudo generar la gráfica de crecimiento para la edad (2-20 años).",
        'height_chart_2_to_20': height_chart_2_to_20 if height_chart_2_to_20 else "No se pudo generar la gráfica de altura para la edad (2-20 años).",
        'bmi_chart_2_to_20': bmi_chart_2_to_20 if bmi_chart_2_to_20 else "No se pudo generar la gráfica de IMC para la edad (2-20 años).",
        'growth_chart_girls_2_to_20': growth_chart_girls_2_to_20 if growth_chart_girls_2_to_20 else "No se pudo generar la gráfica de peso para la edad (2-20 años, niñas).",
        'height_chart_girls_2_to_20': height_chart_girls_2_to_20 if height_chart_girls_2_to_20 else "No se pudo generar la gráfica de altura para la edad (2-20 años, niñas).",
        'bmi_chart_girls_2_to_20': bmi_chart_girls_2_to_20 if bmi_chart_girls_2_to_20 else "No se pudo generar la gráfica de IMC para la edad (2-20 años, niñas)."
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

@login_required
@custom_login_required
def aggEstatura(request,idPat):
    if request.method == 'POST':
        paciente  = Patient.objects.get(idPat=idPat)
        estatura_mom=request.POST['estatura_mom']
        estatura_dad=request.POST['estatura_dad']
        newEstatura = EstaturasRep.objects.create(
            paciente = paciente,
            estatura_mom = estatura_mom,
            estatura_dad = estatura_dad
        )
        messages.success(request,'Información agregada correctamente')
        return redirect('doc_patient', idPat=idPat)
    else:
        messages.error(request, 'No se pudo agregar la información')
        return redirect('doc_patient', idPat=idPat)

@login_required
@custom_login_required
def editEstatura(request, idPat):
    if request.method=='POST':
        idest=request.POST['idest']
        estatura_mom = request.POST['estatura_mom']
        estatura_dad = request.POST['estatura_dad']
        editEstatura = EstaturasRep.objects.get(idest=idest)
        editEstatura.estatura_mom = estatura_mom
        editEstatura.estatura_dad = estatura_dad
        editEstatura.save()
        messages.success(request, 'Información editada correctamente')
        return redirect('doc_patient', idPat=idPat)
    else:
        messages.error(request, 'No se pudo guardar la información')
        return redirect('doc_patient', idPat=idPat)


@login_required
@custom_login_required
def aggCurva(request, idPat):
    if request.method == 'POST':
        try:
            paciente = Patient.objects.get(idPat=idPat)
        except Patient.DoesNotExist:
            messages.error(request, 'Paciente no encontrado.')
            return redirect('doc_patient', idPat=idPat)

        estatura_pat = request.POST.get('estatura_pat')
        peso = request.POST.get('peso')
        IMC = request.POST.get('IMC')
        per_enc = request.POST.get('per_enc', None)

        # Convertir valores a Decimal
        try:
            estatura_pat = Decimal(estatura_pat)
            peso = Decimal(peso)
            IMC = Decimal(IMC)
            if per_enc:
                per_enc = Decimal(per_enc)
            else:
                per_enc = None
        except InvalidOperation:
            messages.error(request, 'Por favor, ingrese valores válidos para todos los campos.')
            return redirect('doc_patient', idPat=idPat)

        # Calcular la edad del paciente en meses
        birth_date = paciente.birthPat
        today = date.today()

        # Calcular la diferencia en años y meses
        age_years = today.year - birth_date.year
        age_months = today.month - birth_date.month

        # Ajustar si el mes de nacimiento es mayor que el mes actual
        if age_months < 0:
            age_years -= 1
            age_months += 12

        total_months = (age_years * 12) + age_months

        # Representar la edad en formato decimal (total meses)
        age_pat = Decimal(total_months)

        try:
            newCurva = Curvas.objects.create(
                paciente=paciente,
                estatura_pat=estatura_pat,
                peso=peso,
                IMC=IMC,
                per_enc=per_enc,
                age_pat=age_pat
            )
            messages.success(request, 'Dato registrado correctamente')
        except Exception as e:
            messages.error(request, f'Error al registrar el dato: {e}')

        return redirect('doc_patient', idPat=idPat)
    else:
        messages.error(request, 'No se pudo ingresar la información')
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
    patbdd = Patient.objects.all()
    mombdd = MadreCita.objects.all()
    dadbdd = PadreCita.objects.all()

    def calculate_age(birthdate):
        today = date.today()
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    for madre in mombdd:
        madre.age_years = calculate_age(madre.age_mom)

    for padre in dadbdd:
        padre.age_years = calculate_age(padre.age_fat)

    return render(request, 'rep/parents.html', {'pacientes': patbdd, 'madres': mombdd, 'padres': dadbdd})

@login_required
@custom_login_required
def editMadre(request, id):
    madre = get_object_or_404(MadreCita, id=id)
    if request.method == 'POST':
        madre.nom_mom = request.POST['nom_mom']
        madre.ape_mom = request.POST['ape_mom']
        madre.es_cimom = request.POST['es_cimom']
        madre.age_mom = request.POST['age_mom']
        madre.hij_mom = request.POST['hij_mom']
        madre.act_mom = request.POST['act_mom']
        madre.correo_mom = request.POST['correo_mom']
        madre.save()
        messages.success(request, 'Información de la madre actualizada correctamente.')
        return redirect('representantesLista')
    else:
        return redirect('error_p')

@login_required
@custom_login_required
def editPadre(request, id):
    padre = get_object_or_404(PadreCita, id=id)
    if request.method == 'POST':
        padre.nom_fat = request.POST['nom_fat']
        padre.ape_fat = request.POST['ape_fat']
        padre.act_fat = request.POST['act_fat']
        padre.age_fat = request.POST['age_fat']
        padre.save()
        messages.success(request, 'Información del padre actualizada correctamente.')
        return redirect('representantesLista')
    else:
        return redirect('error_p')

@login_required
@custom_login_required
def aggMom(request):
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
        return redirect('representantesLista')
@login_required
@custom_login_required
def aggDad(request):
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
        return redirect('representantesLista')

@login_required
@custom_login_required
def deleteMadre(request, id):
    madre = get_object_or_404(MadreCita, id=id)
    madre.delete()
    messages.success(request, 'Información de la madre eliminada correctamente.')
    return redirect('representantesLista')

@login_required
@custom_login_required
def deletePadre(request, id):
    padre = get_object_or_404(PadreCita, id=id)
    padre.delete()
    messages.success(request, 'Información del padre eliminada correctamente.')
    return redirect('representantesLista')

#PÁGINA REPRESENTANTES FINAL
