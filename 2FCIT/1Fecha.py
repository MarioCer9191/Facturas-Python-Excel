import os
import csv

def extraer_fechas_csv():
    # Carpeta raíz (Facturas)
    raiz = os.path.dirname(os.path.dirname(__file__))

    # Archivo de entrada en la carpeta raíz
    archivo_csv = os.path.join(raiz, "PDFRaw.csv")

    # Archivo de salida en la carpeta 2FCIT
    archivo_salida = os.path.join(raiz, "2FCIT", "Fecha.csv")

    if not os.path.exists(archivo_csv):
        print(f"❌ No se encontró el archivo {archivo_csv}")
        return

    with open(archivo_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Ajusta el nombre de la columna según corresponda
        fechas = [row["FechaEmision"] for row in reader if row.get("FechaEmision")]

    # Crear carpeta FCIT si no existe
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)

    with open(archivo_salida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["FechaEmision"])  # encabezado
        for fecha in fechas:
            writer.writerow([fecha])

    print(f" Extracción de fechas completada. Resultados en: {archivo_salida}")

if __name__ == "__main__":
    extraer_fechas_csv()
