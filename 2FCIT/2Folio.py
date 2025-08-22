import os
import csv
import re  # para filtrar solo números

def extraer_folios_csv():
    # Carpeta raíz (Facturas)
    raiz = os.path.dirname(os.path.dirname(__file__))

    # Archivo de entrada en la carpeta raíz
    archivo_csv = os.path.join(raiz, "PDFRaw.csv")

    # Archivo de salida en la carpeta 2FCIT
    archivo_salida = os.path.join(raiz, "2FCIT", "Folio.csv")

    if not os.path.exists(archivo_csv):
        print(f"❌ No se encontró el archivo {archivo_csv}")
        return

    folios = []
    with open(archivo_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            serie = row.get("Serie", "").strip()
            clave = row.get("Clave_1", "").strip()
            
            # Unificar
            combinado = serie + clave
            
            # Filtrar solo números
            solo_numeros = re.sub(r"\D", "", combinado)
            
            # Tomar últimos 5 dígitos
            folio = solo_numeros[-5:] if solo_numeros else ""
            folios.append(folio)

    # Crear carpeta FCIT si no existe
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)

    # Escribir archivo de salida
    with open(archivo_salida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Folio"])  # encabezado
        for folio in folios:
            writer.writerow([folio])

    print(f" Extracción de folios completada. Resultados en: {archivo_salida}")

if __name__ == "__main__":
    extraer_folios_csv()
