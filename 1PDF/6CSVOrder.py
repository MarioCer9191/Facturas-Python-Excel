import os
import csv
import json

# ================================
# Configuración de rutas
# ================================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RUTA_CSV_ORIGINAL = os.path.join(RAIZ, "1PDF", "FACT1.csv")
RUTA_CSV_EXTRAIDO = os.path.join(RAIZ, "1PDF", "FACT2.csv")
RUTA_JSON_CATALOGO = os.path.join(RAIZ, "1PDF", "CATALOGO.json")

# ================================
# Mapeo de columnas
# ================================
COLUMNAS_MAP = {
    "Fecha": "FECHA",
    "Folio": "FOLIO",
    "NombreArchivo": "FOLIO FISCAL",
    "RFCEmisor": "RFC",
    "NombreEmisor": "CONCEPTO",
    "Subtotal": "IMPORTE",
    "IVA16": "IVA",
    "Total": "TOTAL",
    "ClaveProdServ": "ClaveProdServ"
}

# ================================
# Cargar catálogo y crear diccionario clave_producto -> descripcion
# ================================
def cargar_catalogo():
    if not os.path.exists(RUTA_JSON_CATALOGO):
        print(f"❌ No se encontró el archivo: {RUTA_JSON_CATALOGO}")
        return {}
    with open(RUTA_JSON_CATALOGO, "r", encoding="utf-8") as f:
        catalogo = json.load(f)
    return {str(item["clave_producto"]): item["descripcion"] for item in catalogo if "clave_producto" in item and "descripcion" in item}

# ================================
# Leer CSV original y generar CSV nuevo
# ================================
def procesar_csv():
    filas_extraidas = []
    catalogo_dict = cargar_catalogo()

    with open(RUTA_CSV_ORIGINAL, "r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            nueva_fila = {}
            for col_original, col_nueva in COLUMNAS_MAP.items():
                nueva_fila[col_nueva] = fila.get(col_original, "")
            clave_prod_serv = str(fila.get("ClaveProdServ", "")).strip()
            nueva_fila["CATEGORIA"] = catalogo_dict.get(clave_prod_serv, "")
            filas_extraidas.append(nueva_fila)

    # Guardar CSV nuevo con columna CATEGORIA
    columnas_final = list(COLUMNAS_MAP.values()) + ["CATEGORIA"]
    with open(RUTA_CSV_EXTRAIDO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas_final)
        writer.writeheader()
        writer.writerows(filas_extraidas)

    print(f"✅ CSV generado: {RUTA_CSV_EXTRAIDO}")

# ================================
# Ejecutar script
# ================================
if __name__ == "__main__":
    if os.path.exists(RUTA_CSV_ORIGINAL):
        procesar_csv()
    else:
        print(f"❌ No se encontró el archivo: {RUTA_CSV_ORIGINAL}")