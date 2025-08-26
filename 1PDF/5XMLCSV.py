import os
import csv
import xml.etree.ElementTree as ET

# ================================
# Configuración de rutas
# ================================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_XML = os.path.join(RAIZ, "AgregarFacturas")
RUTA_CSV = os.path.join(RAIZ, "1PDF", "FACT1.csv")

# ================================
# Columnas para el CSV
# ================================
COLUMNAS = [
    "NombreArchivo",  # <-- nombre del archivo XML
    "Folio", "Fecha", "NombreEmisor", "RFCEmisor",
    "NombreReceptor", "RFCReceptor", "Subtotal", "IVA16", "Total",
    "ClaveProdServ"   # <-- NUEVO: clave del producto/servicio
]

# ================================
# Función para extraer datos de un XML
# ================================
def extraer_datos_xml(ruta_xml):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()

    # Espacio de nombres CFDI 4.0
    ns = {'cfdi': 'http://www.sat.gob.mx/cfd/4'}

    datos = {}

    # Capturar el nombre del archivo XML
    datos["NombreArchivo"] = os.path.basename(ruta_xml)

    # Comprobante
    datos["Folio"] = root.attrib.get("Folio", "")
    datos["Fecha"] = root.attrib.get("Fecha", "")

    # Emisor
    emisor = root.find("cfdi:Emisor", ns)
    if emisor is not None:
        datos["NombreEmisor"] = emisor.attrib.get("Nombre", "")
        datos["RFCEmisor"] = emisor.attrib.get("Rfc", "")

    # Receptor
    receptor = root.find("cfdi:Receptor", ns)
    if receptor is not None:
        datos["NombreReceptor"] = receptor.attrib.get("Nombre", "")
        datos["RFCReceptor"] = receptor.attrib.get("Rfc", "")

    # Subtotal y Total
    datos["Subtotal"] = root.attrib.get("SubTotal", "")
    datos["Total"] = root.attrib.get("Total", "")

    # IVA16 (sumar todos los traslados de tipo IVA)
    iva_total = 0.0
    impuestos = root.find("cfdi:Impuestos", ns)
    if impuestos is not None:
        traslados = impuestos.find("cfdi:Traslados", ns)
        if traslados is not None:
            for traslado in traslados.findall("cfdi:Traslado", ns):
                tasa = traslado.attrib.get("TasaOCuota", "")
                if tasa and tasa.strip() != "":
                    try:
                        if float(tasa) == 0.16:  # IVA 16%
                            importe_str = traslado.attrib.get("Importe", "0")
                            importe = float(importe_str) if importe_str.strip() != "" else 0.0
                            iva_total += importe
                    except ValueError:
                        pass  # Si tasa no es convertible, ignora
    datos["IVA16"] = f"{iva_total:.2f}"

    # ================================
    # NUEVO: Capturar ClaveProdServ y su valor numérico
    # ================================
    concepto = root.find("cfdi:Conceptos/cfdi:Concepto", ns)
    if concepto is not None:
        datos["ClaveProdServ"] = concepto.attrib.get("ClaveProdServ", "")

    return datos

# ================================
# Generar CSV consolidado
# ================================
if __name__ == "__main__":
    filas = []
    for archivo in os.listdir(CARPETA_XML):
        if archivo.lower().endswith(".xml"):
            ruta_xml = os.path.join(CARPETA_XML, archivo)
            try:
                fila = extraer_datos_xml(ruta_xml)
                filas.append(fila)
            except Exception as e:
                print(f"❌ Error procesando {archivo}: {e}")

    # Guardar CSV
    with open(RUTA_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        writer.writeheader()
        writer.writerows(filas)

    print(f"✅ CSV consolidado generado: {RUTA_CSV}")