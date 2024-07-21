import os
import django
import sys

# Configurar el entorno Django
sys.path.append('C:/Users/Carlos Colcha/Documents/DJANGO EXAMPLES/Tesis/RecTes')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tesis.settings')
django.setup()

from Aplicaciones.Historiales.models import medicina  # Asegúrate de que esta ruta sea correcta

# Lista de medicamentos
medicamentos = [
    {"nombregen_med": "Acetaminofen+Clorferamina+Pseudoefedrina", "nombrecom_med": "Acetaminofen", "tipo_med": "Tab#"},
    {"nombregen_med": "Hedera Helix", "nombrecom_med": "HEDILAR JBE", "tipo_med": "Fsco#"},
    {"nombregen_med": "Ibuprofeno", "nombrecom_med": "IBUPROFENO MK", "tipo_med": "Tab#"},
    {"nombregen_med": "Amoxicilina", "nombrecom_med": "AMOXIL", "tipo_med": "Cap#"},
    {"nombregen_med": "Clorfeniramina", "nombrecom_med": "CLORTRIMETON", "tipo_med": "Tab#"},
    {"nombregen_med": "Loratadina", "nombrecom_med": "CLARITIN", "tipo_med": "Tab#"},
    {"nombregen_med": "Paracetamol", "nombrecom_med": "TYLENOL", "tipo_med": "Tab#"},
    {"nombregen_med": "Omeprazol", "nombrecom_med": "PRILOSEC", "tipo_med": "Cap#"},
    {"nombregen_med": "Esomeprazol", "nombrecom_med": "NEXIUM", "tipo_med": "Cap#"},
    {"nombregen_med": "Levotiroxina", "nombrecom_med": "SYNTHROID", "tipo_med": "Tab#"},
    {"nombregen_med": "Atorvastatina", "nombrecom_med": "LIPITOR", "tipo_med": "Tab#"},
    {"nombregen_med": "Metformina", "nombrecom_med": "GLUCOPHAGE", "tipo_med": "Tab#"},
    {"nombregen_med": "Amlodipino", "nombrecom_med": "NORVASC", "tipo_med": "Tab#"},
    {"nombregen_med": "Salmeterol+Fluticasona", "nombrecom_med": "ADVAIR DISKUS", "tipo_med": "Inh#"},
    {"nombregen_med": "Prednisona", "nombrecom_med": "DELTASONE", "tipo_med": "Tab#"},
    {"nombregen_med": "Clindamicina", "nombrecom_med": "CLEOCIN", "tipo_med": "Cap#"},
    {"nombregen_med": "Sulfametoxazol+Trimetoprima", "nombrecom_med": "BACTRIM", "tipo_med": "Tab#"},
    {"nombregen_med": "Ciprofloxacino", "nombrecom_med": "CIPRO", "tipo_med": "Tab#"},
    {"nombregen_med": "Azitromicina", "nombrecom_med": "ZITHROMAX", "tipo_med": "Tab#"},
    {"nombregen_med": "Albuterol", "nombrecom_med": "PROVENTIL", "tipo_med": "Inh#"},
    {"nombregen_med": "Furosemida", "nombrecom_med": "LASIX", "tipo_med": "Tab#"},
    {"nombregen_med": "Simvastatina", "nombrecom_med": "ZOCOR", "tipo_med": "Tab#"},
    {"nombregen_med": "Lisinopril", "nombrecom_med": "PRINIVIL", "tipo_med": "Tab#"},
    {"nombregen_med": "Rosuvastatina", "nombrecom_med": "CRESTOR", "tipo_med": "Tab#"},
    {"nombregen_med": "Hidroclorotiazida", "nombrecom_med": "MICROZIDE", "tipo_med": "Cap#"},
    {"nombregen_med": "Metoprolol", "nombrecom_med": "LOPRESSOR", "tipo_med": "Tab#"},
    {"nombregen_med": "Carvedilol", "nombrecom_med": "COREG", "tipo_med": "Tab#"},
    {"nombregen_med": "Atenolol", "nombrecom_med": "TENORMIN", "tipo_med": "Tab#"},
    {"nombregen_med": "Valsartán", "nombrecom_med": "DIOVAN", "tipo_med": "Tab#"},
    {"nombregen_med": "Losartán", "nombrecom_med": "COZAAR", "tipo_med": "Tab#"},
    {"nombregen_med": "Propranolol", "nombrecom_med": "INDERAL", "tipo_med": "Tab#"},
    {"nombregen_med": "Diltiazem", "nombrecom_med": "CARDIZEM", "tipo_med": "Tab#"},
    {"nombregen_med": "Verapamilo", "nombrecom_med": "CALAN", "tipo_med": "Tab#"},
    {"nombregen_med": "Enalapril", "nombrecom_med": "VASOTEC", "tipo_med": "Tab#"},
    {"nombregen_med": "Ranitidina", "nombrecom_med": "ZANTAC", "tipo_med": "Tab#"},
    {"nombregen_med": "Famotidina", "nombrecom_med": "PEPCID", "tipo_med": "Tab#"},
    {"nombregen_med": "Metoclopramida", "nombrecom_med": "REGLAN", "tipo_med": "Tab#"},
    {"nombregen_med": "Domperidona", "nombrecom_med": "MOTILIUM", "tipo_med": "Tab#"},
    {"nombregen_med": "Clonazepam", "nombrecom_med": "KLONOPIN", "tipo_med": "Tab#"},
    {"nombregen_med": "Diazepam", "nombrecom_med": "VALIUM", "tipo_med": "Tab#"},
    {"nombregen_med": "Lorazepam", "nombrecom_med": "ATIVAN", "tipo_med": "Tab#"},
    {"nombregen_med": "Alprazolam", "nombrecom_med": "XANAX", "tipo_med": "Tab#"},
    {"nombregen_med": "Fluoxetina", "nombrecom_med": "PROZAC", "tipo_med": "Cap#"},
    {"nombregen_med": "Paroxetina", "nombrecom_med": "PAXIL", "tipo_med": "Tab#"},
    {"nombregen_med": "Sertralina", "nombrecom_med": "ZOLOFT", "tipo_med": "Tab#"},
    {"nombregen_med": "Citalopram", "nombrecom_med": "CELEXA", "tipo_med": "Tab#"},
    {"nombregen_med": "Escitalopram", "nombrecom_med": "LEXAPRO", "tipo_med": "Tab#"},
    {"nombregen_med": "Bupropión", "nombrecom_med": "WELLBUTRIN", "tipo_med": "Tab#"},
    {"nombregen_med": "Venlafaxina", "nombrecom_med": "EFFEXOR", "tipo_med": "Cap#"},
    {"nombregen_med": "Duloxetina", "nombrecom_med": "CYMBALTA", "tipo_med": "Cap#"},
    {"nombregen_med": "Mirtazapina", "nombrecom_med": "REMERON", "tipo_med": "Tab#"},
    {"nombregen_med": "Amitriptilina", "nombrecom_med": "ELAVIL", "tipo_med": "Tab#"},
    {"nombregen_med": "Nortriptilina", "nombrecom_med": "PAMELOR", "tipo_med": "Cap#"},
    {"nombregen_med": "Desvenlafaxina", "nombrecom_med": "PRISTIQ", "tipo_med": "Tab#"},
    {"nombregen_med": "Trazodona", "nombrecom_med": "DESYREL", "tipo_med": "Tab#"},
    {"nombregen_med": "Quetiapina", "nombrecom_med": "SEROQUEL", "tipo_med": "Tab#"},
    {"nombregen_med": "Olanzapina", "nombrecom_med": "ZYPREXA", "tipo_med": "Tab#"},
    {"nombregen_med": "Risperidona", "nombrecom_med": "RISPERDAL", "tipo_med": "Tab#"},
    {"nombregen_med": "Aripiprazol", "nombrecom_med": "ABILIFY", "tipo_med": "Tab#"},
    {"nombregen_med": "Lamotrigina", "nombrecom_med": "LAMICTAL", "tipo_med": "Tab#"},
    {"nombregen_med": "Valproato", "nombrecom_med": "DEPAKOTE", "tipo_med": "Tab#"},
    {"nombregen_med": "Carbamazepina", "nombrecom_med": "TEGRETOL", "tipo_med": "Tab#"},
    {"nombregen_med": "Oxcarbazepina", "nombrecom_med": "TRILEPTAL", "tipo_med": "Tab#"},
    {"nombregen_med": "Topiramato", "nombrecom_med": "TOPAMAX", "tipo_med": "Tab#"},
    {"nombregen_med": "Gabapentina", "nombrecom_med": "NEURONTIN", "tipo_med": "Cap#"},
    {"nombregen_med": "Pregabalina", "nombrecom_med": "LYRICA", "tipo_med": "Cap#"},
    {"nombregen_med": "Levetiracetam", "nombrecom_med": "KEPPRA", "tipo_med": "Tab#"},
    {"nombregen_med": "Fenitoína", "nombrecom_med": "DILANTIN", "tipo_med": "Cap#"},
    {"nombregen_med": "Fenobarbital", "nombrecom_med": "LUMINAL", "tipo_med": "Tab#"},
    {"nombregen_med": "Primidona", "nombrecom_med": "MYSOLINE", "tipo_med": "Tab#"},
    {"nombregen_med": "Etosuximida", "nombrecom_med": "ZARONTIN", "tipo_med": "Cap#"},
    {"nombregen_med": "Tiagabina", "nombrecom_med": "GABITRIL", "tipo_med": "Tab#"},
    {"nombregen_med": "Zonisamida", "nombrecom_med": "ZONEGRAN", "tipo_med": "Cap#"},
    {"nombregen_med": "Lacosamida", "nombrecom_med": "VIMPAT", "tipo_med": "Tab#"},
    {"nombregen_med": "Clobazam", "nombrecom_med": "ONFI", "tipo_med": "Tab#"},
    {"nombregen_med": "Rufinamida", "nombrecom_med": "BANZEL", "tipo_med": "Tab#"},
    {"nombregen_med": "Perampanel", "nombrecom_med": "FYCOMPA", "tipo_med": "Tab#"},
    {"nombregen_med": "Brivaracetam", "nombrecom_med": "BRIVIACT", "tipo_med": "Tab#"},
    {"nombregen_med": "Stiripentol", "nombrecom_med": "DIACOMIT", "tipo_med": "Cap#"},
    {"nombregen_med": "Cannabidiol", "nombrecom_med": "EPIDIOLEX", "tipo_med": "Liq#"},
    {"nombregen_med": "Vigabatrina", "nombrecom_med": "SABRIL", "tipo_med": "Tab#"},
]

# Inserción de datos con verificación de existencia
for medicamento in medicamentos:
    if not medicina.objects.filter(nombrecom_med=medicamento["nombrecom_med"]).exists():
        medicina.objects.create(
            nombregen_med=medicamento["nombregen_med"],
            nombrecom_med=medicamento["nombrecom_med"],
            tipo_med=medicamento["tipo_med"]
        )

print("Medicamentos insertados correctamente.")
