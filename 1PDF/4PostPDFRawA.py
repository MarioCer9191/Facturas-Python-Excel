import os
import re
import csv

def generar_csv():
    # Carpeta actual = ubicación de este script
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))

    # Ir un nivel arriba para llegar a la carpeta raíz "Facturas"
    raiz = os.path.dirname(carpeta_actual)

    archivo_entrada = os.path.join(raiz, "PDFraw.txt")
    archivo_salida = os.path.join(carpeta_actual, "4PostPDFRawA.csv")

    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encontró el archivo en: {archivo_entrada}")
        return

    with open(archivo_entrada, "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar facturas
    separador_patron = re.compile(r"--- Factura: (.+?) ---(.*?)(?=--- Factura:|$)", re.DOTALL)
    invoice_blocks = separador_patron.findall(contenido)
    print(f"📄 Procesando {len(invoice_blocks)} facturas...")

    filas_csv = []
    for i, (_, bloque) in enumerate(invoice_blocks, start=1):
        fecha = re.search(r'\b\d{4}-\d{2}-\d{2}\b', bloque)
        folio = re.search(r'Folio:\s*([^\n]+)', bloque)
        folio_fiscal = re.search(r'Folio fiscal:\s*([^\s\n]+)', bloque)
        emisor = re.search(r'Nombre emisor:\s*([^\n]+)', bloque)
        subtotal = re.search(r'Subtotal \$\s*([\d\.,]+)', bloque)
        iva = re.search(r'IVA [\d\.,]+% \$\s*([\d\.,]+)', bloque)
        total = re.search(r'Total \$\s*([\d\.,]+)', bloque)

        filas_csv.append([
            fecha.group(0) if fecha else "",
            folio.group(1).strip() if folio else "",
            folio_fiscal.group(1).strip() if folio_fiscal else "",
            emisor.group(1).strip() if emisor else "",
            subtotal.group(1).replace(",", "") if subtotal else "0",
            iva.group(1).replace(",", "") if iva else "0",
            total.group(1).replace(",", "") if total else "0",
        ])

    # Guardar CSV en la carpeta donde está el script
    with open(archivo_salida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["FechaEmision","Folio","FolioFiscal","NombreEmisor","Subtotal","IVA_Trasladado","Total"])
        writer.writerows(filas_csv)

    print(f" CSV generado en: {archivo_salida}")


if __name__ == "__main__":
    generar_csv()
