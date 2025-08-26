# extraer_factura.py
import os
import re
import json

# Carpeta donde están los TXT
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_TXT = os.path.join(RAIZ, "AgregarFacturas")
CARPETA_JSON = os.path.join(RAIZ, "AgregarFacturas")

def extraer_datos(texto, nombre_archivo):
    datos = {}

    # Nombre del archivo
    datos["NombreArchivo"] = nombre_archivo

    # Nombre emisor
    emisor = re.search(r"Nombre\s*emisor:\s*([\s\S]*?)Folio:", texto, re.IGNORECASE)
    if emisor:
        datos["NombreEmisor"] = " ".join(emisor.group(1).split()).upper()

    # Folio
    folio = re.search(r"Folio:\s*(\d+)", texto)
    if folio:
        datos["Folio"] = folio.group(1)

    # RFC emisor
    rfc = re.search(r"RFC\s*emisor:\s*([A-Z0-9]+)", texto)
    if rfc:
        datos["RFCEmisor"] = rfc.group(1)

    # Código postal + fecha + hora de emisión
    cod_fecha = re.search(r"Código\s*postal,\s*fecha\s*y\s*hora\s*de\s*emisión:\s*([\s\S]*?)Efecto", texto, re.IGNORECASE)
    if cod_fecha:
        datos["CodigoFechaHoraEmision"] = " ".join(cod_fecha.group(1).split())

    # Objeto impuesto (captura hasta salto de línea o espacio extra)
    obj_imp = re.search(r"Objeto\s*impuesto\s*[:\s]*([\d]{8})", texto, re.IGNORECASE)
    if obj_imp:
        datos["ObjetoImpuesto"] = obj_imp.group(1)

    # Subtotal (si no existe, intenta buscar solo "Subtotal" con cualquier cantidad)
    subtotal = re.search(r"Subtotal\s*\$\s*([\d,]+\.\d{2})", texto)
    if subtotal:
        datos["Subtotal"] = subtotal.group(1).replace(",", "")
    else:
        # Busca solo "Subtotal" seguido de cualquier número
        subtotal_alt = re.search(r"Subtotal\s*\$?\s*([\d,]+)", texto)
        datos["Subtotal"] = subtotal_alt.group(1).replace(",", "") if subtotal_alt else ""

    # IVA trasladado (puede no existir)
    iva = re.search(r"Impuestos\s*trasladados\s*IVA\s*16\.00%\s*\$\s*([\d,]+\.\d{2})", texto, re.IGNORECASE)
    if iva:
        datos["IVA16"] = iva.group(1).replace(",", "")
    else:
        datos["IVA16"] = ""  # Si no existe, deja el campo vacío

    # Total (si no existe, intenta buscar solo "Total" con cualquier cantidad)
    total = re.search(r"Total\s*\$\s*([\d,]+\.\d{2})", texto)
    if total:
        datos["Total"] = total.group(1).replace(",", "")
    else:
        total_alt = re.search(r"Total\s*\$?\s*([\d,]+)", texto)
        datos["Total"] = total_alt.group(1).replace(",", "") if total_alt else ""

    return datos

def procesar_txt():
    for archivo in os.listdir(CARPETA_TXT):
        if archivo.endswith(".txt"):
            ruta_txt = os.path.join(CARPETA_TXT, archivo)
            with open(ruta_txt, "r", encoding="utf-8") as f:
                texto = f.read()

            datos = extraer_datos(texto, archivo)

            # Guardar JSON
            nombre_json = os.path.splitext(archivo)[0] + ".json"
            ruta_json = os.path.join(CARPETA_JSON, nombre_json)
            with open(ruta_json, "w", encoding="utf-8") as fjson:
                json.dump(datos, fjson, ensure_ascii=False, indent=4)

            print(f"✅ Procesado {archivo} → {nombre_json}")

if __name__ == "__main__":
    if os.path.exists(CARPETA_TXT):
        procesar_txt()
    else:
        print(f"⚠ No existe la carpeta: {CARPETA_TXT}")