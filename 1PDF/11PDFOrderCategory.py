import os
import shutil
import csv
import sys

# ================================
# Configuración de rutas
# ================================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_ENTRADA = os.path.join(RAIZ, "1PDF", "PDFOrder.csv")
CARPETA_ORIGEN = os.path.join(RAIZ, "Facturas_Ordenadas")

# ================================
# Main
# ================================
def main():
    # Verificar si el CSV existe
    if not os.path.exists(CSV_ENTRADA):
        print(f"ERROR: No se encontró el archivo CSV: {CSV_ENTRADA}")
        sys.exit(1)

    # Leer el CSV
    try:
        with open(CSV_ENTRADA, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            filas = list(reader)
    except Exception as e:
        print(f"ERROR al leer el CSV: {e}")
        sys.exit(1)

    # Lista para registrar archivos faltantes
    pdfs_faltantes = []

    # Iterar sobre cada fila del CSV
    for fila in filas:
        factura = fila.get("FacturaID", "").strip()
        categoria = fila.get("Categoria", "").strip()

        if not factura or not categoria:
            print(f"Advertencia: fila inválida: {fila}")
            continue

        origen = os.path.join(CARPETA_ORIGEN, factura)
        destino_carpeta = os.path.join(CARPETA_ORIGEN, categoria)
        destino = os.path.join(destino_carpeta, factura)

        # Verificar que el archivo exista
        if not os.path.exists(origen):
            pdfs_faltantes.append(factura)
            print(f"No encontrado: {origen}")
            continue

        # Mover archivo
        try:
            shutil.move(origen, destino)
            print(f"Movido: {factura} -> {categoria}")
        except Exception as e:
            print(f"ERROR al mover {factura}: {e}")

    # Mostrar resumen de archivos faltantes
    if pdfs_faltantes:
        print("\nArchivos listados en CSV pero no encontrados en origen:")
        for f in pdfs_faltantes:
            print(f"- {f}")
    else:
        print("\nTodos los archivos fueron movidos correctamente.")

if __name__ == "__main__":
    main()
