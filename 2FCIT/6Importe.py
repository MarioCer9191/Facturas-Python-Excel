import os
import csv

def extraer_importe_csv():
    # Carpeta raíz = Facturas
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    archivo_entrada = os.path.join(raiz, "PDFRaw.csv")
    archivo_salida = os.path.join(os.path.dirname(__file__), "Importe.csv")  # salida en 2FCIT

    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encontró el archivo {archivo_entrada}")
        return

    with open(archivo_entrada, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        importes = []
        for row in reader:
            try:
                subtotal = float(row.get("Subtotal", "0") or 0)
            except ValueError:
                subtotal = 0
            try:
                descuento = float(row.get("Descuento", "0") or 0)
            except ValueError:
                descuento = 0
            importe = subtotal - descuento
            importes.append(importe)

    # Crear carpeta 2FCIT si no existe
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)

    with open(archivo_salida, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["Importe"])  # encabezado
        for importe in importes:
            writer.writerow([importe])

    print(f" Extracción de Importe completada. Resultados en: {archivo_salida}")

if __name__ == "__main__":
    extraer_importe_csv()
