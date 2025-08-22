import os
import csv

# Rutas
RAIZ = os.path.abspath(os.path.dirname(__file__))
CSV_A = os.path.join(RAIZ, "PDFCategory_A.csv")
CSV_B = os.path.join(RAIZ, "PDFCategory_B.csv")
CSV_FINAL = os.path.join(RAIZ, "PDFCategory_Final.csv")

# Leer CSV y convertir a diccionario por FacturaID (nombre PDF)
def leer_csv_a_dict(ruta):
    data = {}
    with open(ruta, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            key = fila.get("FacturaID") or fila.get("NombreArchivo")  # Ajusta según tu columna de ID
            if key:
                data[key] = fila
    return data

# Merge con prioridad a B
def merge_csv(data_a, data_b):
    final = {}
    for key in set(data_a.keys()).union(data_b.keys()):
        fila_a = data_a.get(key, {})
        fila_b = data_b.get(key, {})
        
        categoria_a = fila_a.get("Categoria", "SIN_CATEGORIA")
        categoria_b = fila_b.get("Categoria", "SIN_CATEGORIA")
        
        # Priorizar B sobre A si B tiene categoría válida
        if categoria_b != "SIN_CATEGORIA":
            categoria_final = categoria_b
        elif categoria_a != "SIN_CATEGORIA":
            categoria_final = categoria_a
        else:
            categoria_final = "SIN_CATEGORIA"
        
        # Crear fila final combinando datos (usar A como base si existe)
        fila_final = fila_a.copy() if fila_a else fila_b.copy()
        fila_final["Categoria"] = categoria_final
        final[key] = fila_final
    
    return final

def main():
    data_a = leer_csv_a_dict(CSV_A)
    data_b = leer_csv_a_dict(CSV_B)
    
    merged = merge_csv(data_a, data_b)
    
    if not merged:
        print("No hay datos para generar el CSV final.")
        return

    # Escribir CSV final
    fieldnames = list(next(iter(merged.values())).keys())
    with open(CSV_FINAL, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for fila in merged.values():
            writer.writerow(fila)
    
    print(f"CSV final generado en {CSV_FINAL}")

if __name__ == "__main__":
    main()
