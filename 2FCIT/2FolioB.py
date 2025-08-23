import os
import pandas as pd

# ============================
# 1. Definir rutas de archivos
# ============================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Carpeta raíz
CARPETA_2FCIT = os.path.join(RAIZ, "2FCIT")
ARCHIVO_CSV = os.path.join(CARPETA_2FCIT, "FolioA.csv")  # Archivo de entrada
ARCHIVO_SALIDA = os.path.join(CARPETA_2FCIT, "Folio.csv")  # Archivo de salida

# Crear carpeta de salida si no existe
os.makedirs(CARPETA_2FCIT, exist_ok=True)

# ============================
# 2. Leer archivo CSV
# ============================
df = pd.read_csv(ARCHIVO_CSV, usecols=["Folio"])

# ============================
# 3. Extraer últimos 5 caracteres
# ============================
def ultimos_5_caracteres(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return ""  # dejar en blanco si es NaN o vacío
    return str(valor)[-5:]  # tomar últimos 5 caracteres

df["Folio"] = df["Folio"].apply(ultimos_5_caracteres)

# ============================
# 4. Guardar archivo de salida
# ============================
df.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")

print(f" Archivo generado: {ARCHIVO_SALIDA}")
