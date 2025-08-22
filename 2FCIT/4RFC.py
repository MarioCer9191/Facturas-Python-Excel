import os
import csv

def extraer_rfc_csv():
    # Carpeta raíz = Facturas
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    archivo_entrada = os.path.join(raiz, "PDFRaw.csv")
    archivo_salida = os.path.join(os.path.dirname(__file__), "RFC.csv")  # salida en 2FCIT

    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encontró el archivo {archivo_entrada}")
        return

    with open(archivo_entrada, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rfcs = [row["RFCEmisor"] for row in reader]

    with open(archivo_salida, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["RFC"])  # encabezado
        for rfc in rfcs:
            writer.writerow([rfc])

    print(f" Extracción de RFC completada. Resultados en: {archivo_salida}")

if __name__ == "__main__":
    extraer_rfc_csv()
