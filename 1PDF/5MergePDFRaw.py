# 5MergePDFRaw.py
import os
import csv

def merge_csvs():
    # Carpeta del script actual (/1PDF)
    carpeta_script = os.path.dirname(os.path.abspath(__file__))
    # Carpeta raíz del proyecto (subir un nivel)
    carpeta_raiz = os.path.dirname(carpeta_script)

    archivo_a = os.path.join(carpeta_script, "4PostPDFRawA.csv")
    archivo_b = os.path.join(carpeta_script, "4PostPDFRawB.csv")
    archivo_salida = os.path.join(carpeta_raiz, "PDFRaw.csv")  # <-- ahora en la raíz

    if not os.path.exists(archivo_a) or not os.path.exists(archivo_b):
        print("❌ No se encontraron ambos CSV en la carpeta 1PDF")
        return

    # Leer CSV A
    data_a = {}
    with open(archivo_a, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get("FolioFiscal", "").replace(".pdf", "").upper().strip()
            if key:
                data_a[key] = {
                    "FechaEmision": row.get("FechaEmision", ""),
                    "Folio": row.get("Folio", ""),
                    "NombreEmisor": row.get("NombreEmisor", ""),
                    "Subtotal": float(row.get("Subtotal", "0") or 0),
                    "IVA_Trasladado": float(row.get("IVA_Trasladado", "0") or 0),
                    "Total": float(row.get("Total", "0") or 0)
                }

    # Leer CSV B
    data_b = {}
    with open(archivo_b, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get("FacturaID", "").replace(".pdf", "").upper().strip()
            if key:
                data_b[key] = row

    # Merge
    merged_rows = []
    for key, row_b in data_b.items():
        # Valores de A si existen
        a_vals = data_a.get(key, {})
        subtotal_a = a_vals.get("Subtotal", 0)
        iva_a = a_vals.get("IVA_Trasladado", 0)
        total_a = a_vals.get("Total", 0)

        # Valores de B
        try:
            subtotal_b = float(row_b.get("Subtotal", "0") or 0)
        except:
            subtotal_b = 0
        try:
            iva_b = float(row_b.get("IVA_Trasladado", "0") or 0)
        except:
            iva_b = 0
        try:
            total_b = float(row_b.get("Total", "0") or 0)
        except:
            total_b = 0

        # Lógica: usar valor que sea >0
        subtotal = subtotal_a if subtotal_a > 0 else subtotal_b
        iva = iva_a if iva_a > 0 else iva_b
        total = total_a if total_a > 0 else total_b

        # Asegurar no negativos
        subtotal = max(subtotal, 0)
        iva = max(iva, 0)
        total = max(total, 0)

        # Crear fila mergeada
        merged_row = row_b.copy()
        merged_row["Subtotal"] = subtotal
        merged_row["IVA_Trasladado"] = iva
        merged_row["Total"] = total

        merged_rows.append(merged_row)

    # Guardar CSV final en la raíz
    if data_b:
        fieldnames = list(data_b[next(iter(data_b))].keys())
        for col in ["Subtotal", "IVA_Trasladado", "Total"]:
            if col not in fieldnames:
                fieldnames.append(col)
    else:
        fieldnames = ["FacturaID", "Subtotal", "IVA_Trasladado", "Total"]

    with open(archivo_salida, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(merged_rows)

    print(f"Merge completado: {archivo_salida}")

if __name__ == "__main__":
    merge_csvs()
