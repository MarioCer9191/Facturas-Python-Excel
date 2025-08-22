import os
import csv

def extraer_iva_csv():
    # Carpeta raíz = Facturas
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    archivo_entrada = os.path.join(raiz, "PDFRaw.csv")
    archivo_salida = os.path.join(os.path.dirname(__file__), "IVA.csv")  # salida en 2FCIT

    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encontró el archivo {archivo_entrada}")
        return

    with open(archivo_entrada, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        ivas = [row.get("IVA_Trasladado", "0") for row in reader]

    # Crear carpeta 2FCIT si no existe
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)

    with open(archivo_salida, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["IVA"])  # encabezado
        for iva in ivas:
            writer.writerow([iva])

    print(f" Extracción de IVA completada. Resultados en: {archivo_salida}")

if __name__ == "__main__":
    extraer_iva_csv()
