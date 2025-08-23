import os
import pandas as pd

# ============================
# 1. Definir rutas de archivos
# ============================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Carpeta raíz
ARCHIVO_CSV = os.path.join(RAIZ, "PDFRaw.csv")  # Archivo de entrada
CARPETA_SALIDA = os.path.join(RAIZ, "2FCIT")
ARCHIVO_SALIDA = os.path.join(CARPETA_SALIDA, "FolioA.csv")  # Archivo de salida final

# Crear carpeta de salida si no existe
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# ============================
# 2. Leer archivo CSV
# ============================
df = pd.read_csv(ARCHIVO_CSV, usecols=["Serie", "Clave_1", "Clave_2"])

# ============================
# 3. Renombrar columnas
# ============================
df = df.rename(columns={
    "Serie": "FolioA",
    "Clave_1": "FolioB",
    "Clave_2": "FolioC"
})

# ============================
# 4. Crear columna Folio concatenando solo valores no nulos
# ============================
def concatenar_filas(row):
    valores = [str(v) for v in [row["FolioA"], row["FolioB"], row["FolioC"]] if pd.notna(v) and str(v).strip() != ""]
    return "".join(valores)

df["Folio"] = df.apply(concatenar_filas, axis=1)

# ============================
# 5. Guardar archivo con las 4 columnas
# ============================
df.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")

print(f" Archivo generado con las 4 columnas (FolioA, FolioB, FolioC, Folio): {ARCHIVO_SALIDA}")
