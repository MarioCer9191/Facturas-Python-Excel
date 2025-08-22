import os
import csv
import json
from collections import Counter

# ================================
# Rutas
# ================================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Carpeta Facturas
CSV_ENTRADA = os.path.join(RAIZ, "1PDF", "PDFCategory.csv")  # Entrada ajustada
CSV_SALIDA = os.path.join(RAIZ, "1PDF", "PDFCategory_A.csv")  # Salida ajustada
CATEGORIAS_JSON = os.path.join(RAIZ, "categorias_backup.json")

# ================================
# Cargar diccionario desde JSON únicamente
# ================================
def cargar_diccionario():
    diccionario = {}

    if os.path.exists(CATEGORIAS_JSON):
        with open(CATEGORIAS_JSON, "r", encoding="utf-8") as f:
            diccionario = json.load(f)
    else:
        print(f"No se encontró {CATEGORIAS_JSON}")

    return diccionario

# ================================
# Asignar categoría usando solo coincidencias exactas
# ================================
def asignar_categoria_fila(fila, diccionario):
    texto_descripcion = str(fila.get("Descripcion", "") or "")
    coincidencias = Counter()

    for categoria, palabras in diccionario.items():
        for palabra in palabras:
            if palabra in texto_descripcion:
                coincidencias[categoria] += 1  # Suma 1 por coincidencia exacta

    if coincidencias:
        return coincidencias.most_common(1)[0][0]
    else:
        return "SIN_CATEGORIA"

# ================================
# Main
# ================================
def main():
    diccionario = cargar_diccionario()
    print("Diccionario cargado:", diccionario)

    if not os.path.exists(CSV_ENTRADA):
        print(f"No se encontró {CSV_ENTRADA}")
        return

    with open(CSV_ENTRADA, "r", encoding="utf-8") as f_in, \
         open(CSV_SALIDA, "w", encoding="utf-8", newline="") as f_out:

        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames + ["Categoria"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row["Categoria"] = asignar_categoria_fila(row, diccionario)
            writer.writerow(row)

    print(f"Archivo final generado en {CSV_SALIDA}")

if __name__ == "__main__":
    main()
