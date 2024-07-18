import os
import pandas as pd
from Aplicaciones.Historiales.models import Cie10  # Asegúrate de ajustar 'Aplicaciones.Historiales' según el nombre de tu aplicación

def import_cie10_from_excel(file_path):
    # Comprobar si el archivo existe
    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe.")
        return

    # Leer el archivo Excel
    df = pd.read_excel(file_path, engine='xlrd')
    print(df.columns)  # Imprimir los nombres de las columnas para verificar

    # Recorrer cada fila del DataFrame y crear instancias del modelo
    for _, row in df.iterrows():
        cod3 = row['COD_3']
        nombrecie = row['DESRIPCION CATEGORIAS DE TRES CARACTERES']  # Usar el nombre correcto

        if pd.notna(cod3) and pd.notna(nombrecie):  # Verifica que los valores no sean NaN
            Cie10.objects.create(
                cod3=cod3,
                nombrecie=nombrecie
            )

# Llama a la función con la ruta al archivo Excel
import_cie10_from_excel(r'C:/Users/Carlos Colcha/Documents/DJANGO EXAMPLES/cie10.xls')
