import pandas as pd
from Aplicaciones.Historiales.models import Cie10

def import_cie10_from_excel(file_path):
    # Leer el archivo Excel
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        cod3 = row['COD_3']
        nombrecie = row['DESRICPION CATEGORIAS DE TRES CARACTERES']

        if pd.notna(cod3) and pd.notna(nombrecie):
            Cie10.objects.create(
                cod3=cod3,
                nombrecie=nombrecie
            )

#ruta al archivo Excel
import_cie10_from_excel('C:\Users\Carlos Colcha\Documents\DJANGO EXAMPLES\cie10.xlsx')
