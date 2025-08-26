import os
import csv
import json

# ================================
# Configuración de rutas
# ================================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RUTA_CSV_ORIGINAL = os.path.join(RAIZ, "1PDF", "FACT2.csv")
RUTA_CSV_PROCESADO = os.path.join(RAIZ, "1PDF", "FACT3.csv")
RUTA_TXT_DESCARTADAS = os.path.join(RAIZ, "FACTURAS_DESCARTADAS.txt")
RUTA_JSON_CATALOGO = os.path.join(RAIZ, "1PDF", "CATALOGO.json")

# ================================
# Columnas a conservar
# ================================
COLUMNAS = [
    "FECHA", "FOLIO", "FOLIO FISCAL", "RFC", "CONCEPTO", "IMPORTE", "IVA", "TOTAL", "CLAVE PRODUCTO", "CATEGORIA"
]

# ================================
# Función para procesar CSV
# ================================
def formato_decimal(valor):
    try:
        return f"{float(valor):.2f}"
    except (ValueError, TypeError):
        return "0.00"

def cargar_catalogo():
    if not os.path.exists(RUTA_JSON_CATALOGO):
        print(f"❌ No se encontró el archivo: {RUTA_JSON_CATALOGO}")
        return {}
    with open(RUTA_JSON_CATALOGO, "r", encoding="utf-8") as f:
        catalogo = json.load(f)
    # Crear diccionario clave_producto -> descripcion
    return {str(item["clave_producto"]): item["descripcion"] for item in catalogo if "clave_producto" in item and "descripcion" in item}

def procesar_csv():
    filas_procesadas = []
    facturas_descartadas = []
    catalogo_dict = cargar_catalogo()

    with open(RUTA_CSV_ORIGINAL, "r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            nueva_fila = {}

            # Fecha se queda igual
            nueva_fila["FECHA"] = fila.get("FECHA", "")

            # Folio: solo los últimos 5 dígitos (o los disponibles)
            folio = fila.get("FOLIO", "")
            nueva_fila["FOLIO"] = folio[-5:] if folio else ""

            # FOLIO FISCAL: solo los primeros 8 dígitos
            folio_fiscal = fila.get("FOLIO FISCAL", "")
            nueva_fila["FOLIO FISCAL"] = folio_fiscal[:8] if folio_fiscal else ""

            # Las demás columnas se mantienen igual, pero IMPORTE, IVA y TOTAL con 2 decimales
            nueva_fila["RFC"] = fila.get("RFC", "")
            nueva_fila["CONCEPTO"] = fila.get("CONCEPTO", "")
            nueva_fila["IMPORTE"] = formato_decimal(fila.get("IMPORTE", ""))
            nueva_fila["IVA"] = formato_decimal(fila.get("IVA", ""))
            nueva_fila["TOTAL"] = formato_decimal(fila.get("TOTAL", ""))

            # Extrae ClaveProdServ y lo coloca como CLAVE PRODUCTO
            clave_prod_serv = fila.get("ClaveProdServ", "")
            nueva_fila["CLAVE PRODUCTO"] = clave_prod_serv

            # Buscar la categoría en el catálogo
            categoria = catalogo_dict.get(str(clave_prod_serv), "")
            nueva_fila["CATEGORIA"] = categoria

            # Reglas de descarte
            justificacion = ""
            if nueva_fila["TOTAL"] == "0.00":
                justificacion = "Factura con valor de 0 pesos (no se incluye en el CSV fiscal)."
            elif categoria == "":
                justificacion = "Factura no categorizada (clave_producto no encontrada en el catálogo)."
            elif categoria.upper() == "DIVERSOS":
                justificacion = "Factura con categoría 'DIVERSOS' (no se incluye en el CSV fiscal)."

            if justificacion:
                factura_txt = (
                    f"FECHA: {nueva_fila['FECHA']}, FOLIO: {nueva_fila['FOLIO']}, FOLIO FISCAL: {nueva_fila['FOLIO FISCAL']}, "
                    f"RFC: {nueva_fila['RFC']}, CONCEPTO: {nueva_fila['CONCEPTO']}, IMPORTE: {nueva_fila['IMPORTE']}, "
                    f"IVA: {nueva_fila['IVA']}, TOTAL: {nueva_fila['TOTAL']}, CLAVE PRODUCTO: {nueva_fila['CLAVE PRODUCTO']}, "
                    f"CATEGORIA: {nueva_fila['CATEGORIA']} | JUSTIFICACION: {justificacion}\n"
                )
                facturas_descartadas.append(factura_txt)
                print(f"⚠ Factura descartada: FOLIO {nueva_fila['FOLIO']} | JUSTIFICACION: {justificacion}")
            else:
                filas_procesadas.append(nueva_fila)

    # Guardar CSV procesado
    with open(RUTA_CSV_PROCESADO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        writer.writeheader()
        writer.writerows(filas_procesadas)

    # Guardar facturas descartadas en TXT con justificación
    if facturas_descartadas:
        if not os.path.exists(os.path.dirname(RUTA_TXT_DESCARTADAS)):
            os.makedirs(os.path.dirname(RUTA_TXT_DESCARTADAS))
        with open(RUTA_TXT_DESCARTADAS, "w", encoding="utf-8") as ftxt:
            ftxt.write("Facturas descartadas (justificación en cada línea):\n\n")
            for factura in facturas_descartadas:
                ftxt.write(factura)

    print(f"✅ CSV procesado generado: {RUTA_CSV_PROCESADO}")
    if facturas_descartadas:
        print(f"⚠ Facturas descartadas registradas en: {RUTA_TXT_DESCARTADAS}")

# ================================
# Ejecutar script
# ================================
if __name__ == "__main__":
    if os.path.exists(RUTA_CSV_ORIGINAL):
        procesar_csv()
    else:
        print(f"❌ No se encontró el archivo: {RUTA_CSV_ORIGINAL}")