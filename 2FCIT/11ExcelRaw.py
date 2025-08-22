import os
import csv

# Rutas
RAIZ = os.path.abspath(os.path.dirname(__file__))
CSV_ENTRADA = os.path.join(RAIZ, "Unificador.csv")
CSV_SALIDA = os.path.join(RAIZ, "ExcelRaw.csv")

def main():
    if not os.path.exists(CSV_ENTRADA):
        print(f"No se encontró el archivo {CSV_ENTRADA}")
        return

    filas_validas = []

    with open(CSV_ENTRADA, "r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames

        for fila in reader:
            total_str = fila.get("Total", "").replace(",", "").strip()
            try:
                total = float(total_str)
            except ValueError:
                total = None  # Ignora si no es número

            if total != 0:  # Solo conservar si total != 0
                filas_validas.append(fila)

    # Guardar CSV filtrado
    with open(CSV_SALIDA, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for fila in filas_validas:
            writer.writerow(fila)

    print(f"Archivo filtrado guardado como {CSV_SALIDA}")

if __name__ == "__main__":
    main()
