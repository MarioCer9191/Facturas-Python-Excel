# 11ExtraerDescripcion_v2.py
import os
import csv
import re

def extraer_descripcion():
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    archivo_entrada = os.path.join(raiz, "PDFraw.txt")
    carpeta_salida = os.path.join(raiz, "1PDF")
    archivo_salida = os.path.join(carpeta_salida, "PDFCategory.csv")

    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encontró el archivo {archivo_entrada}")
        return

    os.makedirs(carpeta_salida, exist_ok=True)

    with open(archivo_entrada, "r", encoding="utf-8") as f:
        data = f.read()

    separador_patron = re.compile(r"--- Factura: (.+?) ---(.*?)(?=--- Factura:|$)", re.DOTALL)
    invoice_blocks = separador_patron.findall(data)
    total_facturas = len(invoice_blocks)
    print(f"💼 Extrayendo información de {total_facturas} facturas...")

    with open(archivo_salida, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["FacturaID", "NombreEmisor", "RFCEmisor", "Descripcion"])

        for factura_id, bloque in invoice_blocks:
            nombre_emisor_match = re.search(r"Nombre emisor:\s*(.+)", bloque)
            nombre_emisor = nombre_emisor_match.group(1).strip() if nombre_emisor_match else ""

            rfc_match = re.search(r"RFC emisor:\s*(\S+)", bloque)
            rfc_emisor = rfc_match.group(1).strip() if rfc_match else ""

            descripcion_match = re.search(
                r"Descripción\s*(.*?)\s*(?:Información Adicional:|Clave del producto|$)", 
                bloque, re.DOTALL | re.IGNORECASE
            )
            descripcion = descripcion_match.group(1).replace("\n", " ").strip() if descripcion_match else ""

            # Convertir todos los campos a mayúsculas antes de escribir
            writer.writerow([
                factura_id.strip().upper(),
                nombre_emisor.upper(),
                rfc_emisor.upper(),
                descripcion.upper()
            ])

    print(f" Archivo PDFCategory.csv generado correctamente en {archivo_salida}")

if __name__ == "__main__":
    extraer_descripcion()
