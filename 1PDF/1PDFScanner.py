# 1PDFScanner.py (ubicado en 1PDF)
import os
from PyPDF2 import PdfReader

def run_pdf_scanner():
    # Carpeta donde se encuentran los PDFs
    carpeta_base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Agregar paquete de facturas")

    # Archivo de salida en la carpeta raíz
    archivo_salida = os.path.join(os.path.dirname(os.path.dirname(__file__)), "PDFraw.txt")

    pdfs_procesados = 0
    pdfs_ignorados = 0

    # Listado de PDFs válidos (excluyendo NO DEDUCIBLES)
    pdf_a_procesar = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(carpeta_base)
        if "NO DEDUCIBLES" not in root.upper()
        for file in files
        if file.lower().endswith(".pdf")
    ]

    total_pdfs = len(pdf_a_procesar)

    # Abrimos el archivo de salida
    with open(archivo_salida, "w", encoding="utf-8") as f_salida:
        for i, ruta_pdf in enumerate(pdf_a_procesar, start=1):
            try:
                reader = PdfReader(ruta_pdf)
                texto = "\n".join(page.extract_text() or "" for page in reader.pages)

                # Separador por factura
                f_salida.write(f"--- Factura: {os.path.basename(ruta_pdf)} ---\n")
                f_salida.write(texto + "\n\n")

                pdfs_procesados += 1
            except Exception as e:
                print(f" Error leyendo {ruta_pdf}: {e}")
                pdfs_ignorados += 1

    # Resumen final
    print(" Extracción completada.")
    print(f"PDFs encontrados: {total_pdfs}")
    print(f"PDFs procesados: {pdfs_procesados}")
    print(f"PDFs ignorados: {pdfs_ignorados}")

if __name__ == "__main__":
    run_pdf_scanner()
