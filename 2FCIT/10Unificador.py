import os
import csv
from Levenshtein import ratio

# Rutas
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Carpeta Facturas
CARPETA_2FCIT = os.path.join(RAIZ, "2FCIT")

CSV_PREUNIFICADOR = os.path.join(CARPETA_2FCIT, "Preunificador.csv")
CSV_PDFCATEGORY = os.path.join(RAIZ, "1PDF", "PDFCategory_Final.csv")
CSV_SALIDA = os.path.join(CARPETA_2FCIT, "Unificador.csv")

UMBRAL_SIMILITUD = 0.70  # Ajustable

def cargar_referencia():
    """
    Carga PDFCategory_Final.csv en un diccionario de referencia:
    NombreEmisor -> Categoria
    """
    referencia = {}
    if not os.path.exists(CSV_PDFCATEGORY):
        print(f" No se encontró el archivo {CSV_PDFCATEGORY}")
        return referencia

    with open(CSV_PDFCATEGORY, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nombre_emisor = row.get("NombreEmisor", "").strip().upper()
            categoria = row.get("Categoria", "SIN_CATEGORIA").strip()
            referencia[nombre_emisor] = categoria
    return referencia

def main():
    referencia = cargar_referencia()
    if not referencia:
        print(" No se pudo cargar la referencia. Abortando.")
        return

    if not os.path.exists(CSV_PREUNIFICADOR):
        print(f" No se encontró el archivo {CSV_PREUNIFICADOR}")
        return

    with open(CSV_PREUNIFICADOR, "r", encoding="utf-8") as f_pre, \
         open(CSV_SALIDA, "w", encoding="utf-8", newline="") as f_out:

        reader = csv.DictReader(f_pre)
        fieldnames = reader.fieldnames + ["Categoria"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            concepto = row.get("Concepto", "").strip().upper()
            mejor_ratio = 0
            categoria_asignada = "SIN_CATEGORIA"

            # Buscar coincidencia más cercana en referencia
            for nombre_ref, cat in referencia.items():
                similitud = ratio(concepto, nombre_ref)
                if similitud > mejor_ratio:
                    mejor_ratio = similitud
                    categoria_asignada = cat

            if mejor_ratio < UMBRAL_SIMILITUD:
                categoria_asignada = "SIN_CATEGORIA"

            row["Categoria"] = categoria_asignada
            writer.writerow(row)

    print(f" Archivo Unificador.csv generado correctamente en {CSV_SALIDA}")

if __name__ == "__main__":
    main()
