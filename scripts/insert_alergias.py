# scripts/insert_alergias.py
import datetime
import os
import django
import sys

# Configurar el entorno Django
sys.path.append('C:/Users/Carlos Colcha/Documents/DJANGO/RecTes')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tesis.settings')
django.setup()

from Aplicaciones.Historiales.models import Alergia  # Asegúrate de que esta ruta sea correcta

# Lista de alergias comunes
alergias_comunes = [
    "Polen",
    "Ácaros del polvo",
    "Caspa de mascotas",
    "Moho",
    "Picaduras de insectos",
    "Leche",
    "Huevos",
    "Pescado",
    "Mariscos",
    "Maní",
    "Frutos secos",
    "Trigo",
    "Soja",
    "Medicamentos",
    "Látex",
    "Níquel",
    "Perfumes",
    "Fragancias",
    "Plantas",
    "Árboles",
    "Hierba",
    "Plumas",
    "Animales de granja",
    "Alimentos procesados",
    "Chocolate",
    "Fresas",
    "Tomates",
    "Cítricos",
    "Manzanas",
    "Peras",
    "Duraznos",
    "Cerezas",
    "Uvas",
    "Kiwi",
    "Alcohol",
    "Conservantes",
    "Colorantes",
    "Aspartame",
    "Gluten",
    "Ajo",
    "Cebolla",
    "Especias",
    "Sulfatos",
    "Cloro",
    "Jabones",
    "Detergentes",
    "Productos de limpieza",
    "Polvo de construcción",
    "Cosméticos",
    "Tabaco",
    "Nueces",
    "Almendras",
    "Anacardos",
    "Avellanas",
    "Pistachos",
    "Camarones",
    "Langostas",
    "Cangrejos",
    "Almejas",
    "Mejillones",
    "Ostras",
    "Salmón",
    "Atún",
    "Trucha",
    "Bacalao",
    "Peces",
    "Carne de res",
    "Carne de cerdo",
    "Carne de pollo",
    "Carne de pavo",
    "Carne de cordero",
    "Legumbres",
    "Garbanzos",
    "Lentejas",
    "Frijoles",
    "Guisantes",
    "Acelgas",
    "Espinacas",
    "Lechuga",
    "Zanahorias",
    "Patatas",
    "Brócoli",
    "Coliflor",
    "Pepinos",
    "Calabacines",
    "Pimientos",
    "Berenjenas",
    "Maíz",
    "Arroz",
    "Avena",
    "Cebada",
    "Centeno",
    "Miel",
    "Gelatina",
    "Caramelos",
    "Galletas",
    "Pasteles",
    "Helado",
    "Yogur",
    "Queso",
    "Mantequilla",
    "Aceite de oliva",
    "Aceite de coco",
    "Aceite de girasol",
    "Aceite de palma"
]

# Inserción de datos con verificación de existencia
for nombre in alergias_comunes:
    if not Alergia.objects.filter(nombreAlergia=nombre).exists():
        Alergia.objects.create(
            creation=datetime.date.today(),
            nombreAlergia=nombre
        )

print("Alergias comunes insertadas correctamente.")
