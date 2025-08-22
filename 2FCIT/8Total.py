import os
import csv

def extraer_total_csv():
    # Carpeta raíz = Facturas
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    archivo_entrada = os.path.join(raiz, "PDFRaw.csv")
    archivo_salida = os.path.join(os.path.dirname(__file__), "Total.csv")  # salida en 2FCIT

    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encontró el archivo {archivo_entrada}")
        return

    with open(archivo_entrada, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        totales = []
        for row in reader:
            try:
                total = float(row.get("Total", "0") or 0)
            except ValueError:
                total = 0
            totales.append(total)

    # Crear carpeta 2FCIT si no existe
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)

    with open(archivo_salida, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["Total"])  # encabezado
        for total in totales:
            writer.writerow([total])

    print(f" Extracción de Total completada. Resultados en: {archivo_salida}")

if __name__ == "__main__":
    extraer_total_csv()
