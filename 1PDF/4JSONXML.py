# generar_xml_desde_json.py
import os
import json
from xml.etree.ElementTree import Element, SubElement, ElementTree

# ============================
# Configuración de rutas
# ============================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_JSON = os.path.join(RAIZ, "AgregarFacturas")
CARPETA_XML = os.path.join(RAIZ, "AgregarFacturas")

if not os.path.exists(CARPETA_XML):
    os.makedirs(CARPETA_XML)

# ============================
# Función para generar XML CFDI
# ============================
def generar_xml(datos_json, ruta_xml, nombre_archivo):
    cfdi = "http://www.sat.gob.mx/cfd/4"
    
    # Obtener la fecha de emisión de forma segura
    codigo_fecha = datos_json.get("CodigoFechaHoraEmision", "")
    if codigo_fecha and len(codigo_fecha.split()) > 1:
        fecha_emision = codigo_fecha.split()[1]
    else:
        fecha_emision = "2025-01-01T00:00:00"

    # Comprobante
    comprobante = Element("cfdi:Comprobante", {
        "Version": "4.0",
        "Fecha": fecha_emision,
        "Folio": datos_json.get("Folio", "0000"),
        "SubTotal": datos_json.get("Subtotal", "0.00"),
        "Total": datos_json.get("Total", "0.00"),
        "TipoDeComprobante": "I",
        "Moneda": "MXN",
        "NombreArchivo": nombre_archivo,
        "ObjetoImpuesto": datos_json.get("ObjetoImpuesto", "00000000"),
        "xmlns:cfdi": cfdi
    })

    # Emisor
    SubElement(comprobante, "cfdi:Emisor", {
        "Nombre": datos_json.get("NombreEmisor", "DESCONOCIDO"),
        "Rfc": datos_json.get("RFCEmisor", "XAXX010101000"),
        "RegimenFiscal": "601"
    })

    # Receptor (temporal, sin datos en el JSON)
    SubElement(comprobante, "cfdi:Receptor", {
        "Nombre": "DESCONOCIDO",
        "Rfc": "XAXX010101000",
        "UsoCFDI": "D01"
    })

    # Conceptos
    conceptos = SubElement(comprobante, "cfdi:Conceptos")
    concepto = SubElement(conceptos, "cfdi:Concepto", {
        "ClaveProdServ": datos_json.get("ObjetoImpuesto", "00000000"),
        "ClaveUnidad": "H87",
        "Cantidad": "1",
        "Descripcion": "Producto o Servicio",
        "ValorUnitario": datos_json.get("Subtotal", "0.00"),
        "Importe": datos_json.get("Subtotal", "0.00")
    })

    impuestos_concepto = SubElement(concepto, "cfdi:Impuestos")
    traslados = SubElement(impuestos_concepto, "cfdi:Traslados")
    SubElement(traslados, "cfdi:Traslado", {
        "Base": datos_json.get("Subtotal", "0.00"),
        "Impuesto": "002",
        "TipoFactor": "Tasa",
        "TasaOCuota": "0.16",
        "Importe": datos_json.get("IVA16", "0.00")
    })

    # Impuestos generales
    impuestos = SubElement(comprobante, "cfdi:Impuestos", {
        "TotalImpuestosTrasladados": datos_json.get("IVA16", "0.00")
    })
    traslados_total = SubElement(impuestos, "cfdi:Traslados")
    SubElement(traslados_total, "cfdi:Traslado", {
        "Base": datos_json.get("Subtotal", "0.00"),
        "Impuesto": "002",
        "TipoFactor": "Tasa",
        "TasaOCuota": "0.16",
        "Importe": datos_json.get("IVA16", "0.00")
    })

    # Guardar XML
    tree = ElementTree(comprobante)
    tree.write(ruta_xml, encoding="utf-8", xml_declaration=True)
    print(f"✅ XML generado: {ruta_xml}")

# ============================
# Procesar todos los JSON
# ============================
def procesar_json():
    for archivo in os.listdir(CARPETA_JSON):
        if archivo.endswith(".json"):
            ruta_json = os.path.join(CARPETA_JSON, archivo)
            with open(ruta_json, "r", encoding="utf-8") as f:
                datos = json.load(f)

            nombre_xml = os.path.splitext(archivo)[0] + ".xml"
            ruta_xml = os.path.join(CARPETA_XML, nombre_xml)
            generar_xml(datos, ruta_xml, archivo)

if __name__ == "__main__":
    procesar_json()