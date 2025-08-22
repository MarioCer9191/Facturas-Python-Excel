# 3Fiscal_CSV.py
import os
import csv

def extraer_fiscal_csv():
    # Ruta base de la carpeta "Facturas"
    raiz = os.path.dirname(os.path.dirname(__file__))
    
    # Archivo de entrada y salida
    archivo_entrada = os.path.join(raiz, "PDFRaw.csv")
    archivo_salida = os.path.join(raiz, "2FCIT", "Fiscal.csv")

    # Validación archivo de entrada
    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encontró el archivo {archivo_entrada}")
        return

    fiscales = []
    with open(archivo_entrada, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            factura_id = row.get("FacturaID", "").strip()
            fiscales.append(factura_id[:8])  # solo primeros 8 caracteres

    # Crear carpeta de salida si no existe
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)

    # Guardar CSV final
    with open(archivo_salida, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["Fiscal"])  # encabezado
        for fiscal in fiscales:
            writer.writerow([fiscal])

    print(f" Extracción de fiscales completada. Resultados en: {archivo_salida}")

if __name__ == "__main__":
    extraer_fiscal_csv()
