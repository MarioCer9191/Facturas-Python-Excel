import os
import csv

def preunificar_csv():
    # Carpeta 2FCIT
    carpeta_2fcit = os.path.dirname(__file__)
    archivo_salida = os.path.join(carpeta_2fcit, "PreUnificador.csv")

    # Archivos CSV intermedios y sus nombres de columna
    archivos_campos = [
        ("Fecha.csv", "Fecha"),
        ("Folio.csv", "Folio"),
        ("Fiscal.csv", "Fiscal"),
        ("RFC.csv", "RFC"),
        ("Concepto.csv", "Concepto"),
        ("Importe.csv", "Importe"),
        ("IVA.csv", "IVA"),
        ("Total.csv", "Total")
    ]

    # Leer todos los archivos intermedios
    listas = []
    for archivo, _ in archivos_campos:
        ruta_archivo = os.path.join(carpeta_2fcit, archivo)
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                listas.append([row[list(reader.fieldnames)[0]] for row in reader])
        else:
            listas.append([])

    # Determinar número total de facturas
    total_facturas = max(len(lst) for lst in listas) if listas else 0

    # Escribir CSV final
    with open(archivo_salida, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        # Escribir encabezado
        writer.writerow([nombre for _, nombre in archivos_campos])
        # Escribir filas
        for idx in range(total_facturas):
            fila = [listas[campo_idx][idx] if idx < len(listas[campo_idx]) else "" 
                    for campo_idx in range(len(archivos_campos))]
            writer.writerow(fila)

    print(f" PreUnificación completada. Resultados en: {archivo_salida}")


if __name__ == "__main__":
    preunificar_csv()
