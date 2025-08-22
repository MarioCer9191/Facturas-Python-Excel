# 4PostPDFRawB.py
import re
import os
import csv

def limpiar_importe(valor):
    """Convierte un string de importe a formato limpio de número (quita comas y espacios)."""
    return valor.replace(',', '').strip() if valor else ""

def generar_csv_extendido_dinamico():
    carpeta_raiz = os.path.join(os.path.dirname(__file__))  # carpeta 1PDF
    archivo_entrada = os.path.join(os.path.dirname(carpeta_raiz), "PDFraw.txt")  # PDFraw.txt en carpeta raíz
    archivo_salida = os.path.join(carpeta_raiz, "4PostPDFRawB.csv")  # CSV dentro de 1PDF

    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encontró el archivo {archivo_entrada}")
        return

    with open(archivo_entrada, "r", encoding="utf-8") as f:
        data = f.read()

    separador_factura = re.compile(r"--- Factura: (.+?) ---(.*?)(?=--- Factura:|$)", re.DOTALL)
    invoice_blocks = separador_factura.findall(data)

    cabeceras_fijas = [
        "FacturaID", "NombreEmisor", "RFCEmisor", "NombreReceptor", "RFCReceptor",
        "CodigoPostalReceptor", "Serie", "FechaEmision", "Moneda", "FormaPago", "MetodoPago",
        "CondicionesPago", "EfectoComprobante", "RegimenFiscalEmisor", "RegimenFiscalReceptor",
        "Exportacion", "Subtotal", "Descuento", "IVA_Trasladado", "Total",
        "CadenaOriginal", "SelloCFDI", "SelloSAT", "FolioFiscal"
    ]

    max_conceptos = 0
    todas_facturas = []

    for factura_id, texto in invoice_blocks:
        fila = {}
        fila["FacturaID"] = factura_id.strip()
        fila["NombreEmisor"] = re.search(r"Nombre emisor:\s*(.+)", texto, re.IGNORECASE).group(1).strip() if re.search(r"Nombre emisor:\s*(.+)", texto, re.IGNORECASE) else ""
        fila["RFCEmisor"] = re.search(r"RFC emisor:\s*([A-Z0-9]+)", texto, re.IGNORECASE).group(1).strip() if re.search(r"RFC emisor:\s*([A-Z0-9]+)", texto, re.IGNORECASE) else ""
        fila["NombreReceptor"] = re.search(r"Nombre receptor:\s*(.+)", texto, re.IGNORECASE).group(1).strip() if re.search(r"Nombre receptor:\s*(.+)", texto, re.IGNORECASE) else ""
        fila["RFCReceptor"] = re.search(r"RFC receptor:\s*([A-Z0-9]+)", texto, re.IGNORECASE).group(1).strip() if re.search(r"RFC receptor:\s*([A-Z0-9]+)", texto, re.IGNORECASE) else ""
        fila["CodigoPostalReceptor"] = re.search(r"Código postal del\s*receptor:\s*(\d+)", texto, re.IGNORECASE).group(1).strip() if re.search(r"Código postal del\s*receptor:\s*(\d+)", texto, re.IGNORECASE) else ""
        fila["Serie"] = re.search(r"Serie:\s*(.+)", texto, re.IGNORECASE).group(1).strip() if re.search(r"Serie:\s*(.+)", texto, re.IGNORECASE) else ""
        fila["FechaEmision"] = re.search(r"(\d{4}-\d{2}-\d{2})", texto).group(1) if re.search(r"(\d{4}-\d{2}-\d{2})", texto) else ""
        fila["Moneda"] = re.search(r"Moneda:\s*(.+)", texto).group(1).strip() if re.search(r"Moneda:\s*(.+)", texto) else ""
        fila["FormaPago"] = re.search(r"Forma de pago:\s*(.+)", texto).group(1).strip() if re.search(r"Forma de pago:\s*(.+)", texto) else ""
        fila["MetodoPago"] = re.search(r"Método de pago:\s*(.+)", texto).group(1).strip() if re.search(r"Método de pago:\s*(.+)", texto) else ""
        fila["CondicionesPago"] = re.search(r"Condiciones de pago:\s*(.+)", texto).group(1).strip() if re.search(r"Condiciones de pago:\s*(.+)", texto) else ""
        fila["EfectoComprobante"] = re.search(r"Efecto de comprobante:\s*(.+)", texto).group(1).strip() if re.search(r"Efecto de comprobante:\s*(.+)", texto) else ""
        fila["RegimenFiscalEmisor"] = re.search(r"Régimen fiscal:\s*(.+)", texto).group(1).strip() if re.search(r"Régimen fiscal:\s*(.+)", texto) else ""
        fila["RegimenFiscalReceptor"] = re.search(r"Régimen fiscal\s*receptor:\s*(.+)", texto).group(1).strip() if re.search(r"Régimen fiscal\s*receptor:\s*(.+)", texto) else ""
        fila["Exportacion"] = re.search(r"Exportación:\s*(.+)", texto).group(1).strip() if re.search(r"Exportación:\s*(.+)", texto) else ""

        fila["Subtotal"] = limpiar_importe(re.search(r"Subtotal \$\s*([\d,]+\.\d{2})", texto).group(1) if re.search(r"Subtotal \$\s*([\d,]+\.\d{2})", texto) else "")
        fila["Descuento"] = limpiar_importe(re.search(r"Descuento \$\s*([\d,]+\.\d{2})", texto).group(1) if re.search(r"Descuento \$\s*([\d,]+\.\d{2})", texto) else "")
        fila["IVA_Trasladado"] = limpiar_importe(re.search(r"Impuestos trasladados IVA [\d\.%]+\s*\$ ([\d,]+\.\d{2})", texto).group(1) if re.search(r"Impuestos trasladados IVA [\d\.%]+\s*\$ ([\d,]+\.\d{2})", texto) else "")
        fila["Total"] = limpiar_importe(re.search(r"Total \$ ([\d,]+\.\d{2})", texto).group(1) if re.search(r"Total \$ ([\d,]+\.\d{2})", texto) else "")

        fila["CadenaOriginal"] = re.search(r"Cadena Original del complemento de certificación digital del SAT:\s*(.+)", texto, re.DOTALL).group(1).strip() if re.search(r"Cadena Original del complemento de certificación digital del SAT:\s*(.+)", texto, re.DOTALL) else ""
        fila["SelloCFDI"] = re.search(r"Sello digital del CFDI:\s*(.+)", texto, re.DOTALL).group(1).strip() if re.search(r"Sello digital del CFDI:\s*(.+)", texto, re.DOTALL) else ""
        fila["SelloSAT"] = re.search(r"Sello digital del SAT:\s*(.+)", texto, re.DOTALL).group(1).strip() if re.search(r"Sello digital del SAT:\s*(.+)", texto, re.DOTALL) else ""
        fila["FolioFiscal"] = re.search(r"Folio fiscal:\s*([A-F0-9\-]+)", texto, re.IGNORECASE).group(1).strip() if re.search(r"Folio fiscal:\s*([A-F0-9\-]+)", texto, re.IGNORECASE) else ""

        conceptos = re.findall(
            r"(\d{5,14})\s+(.+?)\s+(\d+(?:\.\d+)?)\s+([A-Z0-9]+)\s+([0-9,\.]+)\s+([0-9,\.]+)(?:\s+.*?IVA Traslado\s*([0-9,\.]+))?",
            texto, re.DOTALL
        )

        fila["conceptos"] = conceptos
        if len(conceptos) > max_conceptos:
            max_conceptos = len(conceptos)

        todas_facturas.append(fila)

    cabeceras = cabeceras_fijas.copy()
    for i in range(1, max_conceptos + 1):
        cabeceras.extend([f"Clave_{i}", f"Descripcion_{i}", f"Cantidad_{i}", f"Unidad_{i}", f"ValorUnitario_{i}", f"Importe_{i}", f"IVA_{i}"])

    with open(archivo_salida, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=cabeceras)
        writer.writeheader()

        for fila in todas_facturas:
            for i, concepto in enumerate(fila["conceptos"], start=1):
                clave, descripcion, cantidad, unidad, valor_unitario, importe, iva = concepto
                fila[f"Clave_{i}"] = clave.strip()
                fila[f"Descripcion_{i}"] = descripcion.strip()
                fila[f"Cantidad_{i}"] = cantidad.strip()
                fila[f"Unidad_{i}"] = unidad.strip()
                fila[f"ValorUnitario_{i}"] = limpiar_importe(valor_unitario)
                fila[f"Importe_{i}"] = limpiar_importe(importe)
                fila[f"IVA_{i}"] = limpiar_importe(iva)
            for j in range(len(fila["conceptos"]) + 1, max_conceptos + 1):
                fila[f"Clave_{j}"] = ""
                fila[f"Descripcion_{j}"] = ""
                fila[f"Cantidad_{j}"] = ""
                fila[f"Unidad_{j}"] = ""
                fila[f"ValorUnitario_{j}"] = ""
                fila[f"Importe_{j}"] = ""
                fila[f"IVA_{j}"] = ""
            del fila["conceptos"]
            writer.writerow(fila)

    print(f" CSV generado exitosamente en: {archivo_salida}")

if __name__ == "__main__":
    generar_csv_extendido_dinamico()
