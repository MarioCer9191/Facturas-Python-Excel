import pandas as pd
from datetime import datetime
import os
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.styles import numbers

# ================================
# 1. Rutas
# ================================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Carpeta Facturas
CSV_ENTRADA = os.path.join(RAIZ, "2FCIT", "ExcelRaw.csv")  # <-- Cambiado a ExcelRaw.csv
CARPETA_SALIDA = os.path.join(RAIZ, "3EXCEL")
EXCEL_SALIDA = os.path.join(CARPETA_SALIDA, "Facturas_Organizadas.xlsx")

os.makedirs(CARPETA_SALIDA, exist_ok=True)

# ================================
# 2. Leer ExcelRaw.csv
# ================================
df = pd.read_csv(CSV_ENTRADA, encoding="utf-8")

# ================================
# 3. Normalizar columnas
# ================================
df.columns = [col.upper() for col in df.columns]

# Convertir FECHA a datetime
if "FECHA" in df.columns:
    df["FECHA"] = pd.to_datetime(df["FECHA"], dayfirst=True, errors="coerce")

# ================================
# 4. Ordenar por FECHA y CONCEPTO
# ================================
if "CONCEPTO" not in df.columns:
    df["CONCEPTO"] = df.get("NOMBREEMISOR", "")

df = df.sort_values(by=["FECHA", "CONCEPTO"]).reset_index(drop=True)

# ================================
# 5. Crear DataFrame con subtotales por CATEGORIA
# ================================
final_rows = []

for categoria, group in df.groupby("CATEGORIA"):
    for row in group.to_dict("records"):
        final_rows.append(row)

    subtotal = {col: "" for col in df.columns}
    subtotal["CONCEPTO"] = f"SUBTOTAL {categoria}"
    if "IMPORTE" in df.columns:
        subtotal["IMPORTE"] = group["IMPORTE"].sum()
    if "IVA" in df.columns:
        subtotal["IVA"] = group["IVA"].sum()
    if "TOTAL" in df.columns:
        subtotal["TOTAL"] = group["TOTAL"].sum()

    final_rows.append(subtotal)
    final_rows.append({})  # fila en blanco

df_final = pd.DataFrame(final_rows)

# ================================
# 6. Formato FECHA seguro
# ================================
if "FECHA" in df_final.columns:
    df_final["FECHA"] = pd.to_datetime(df_final["FECHA"], errors="coerce")
    df_final["FECHA"] = df_final["FECHA"].apply(
        lambda x: x.strftime("%d-%m-%Y") if pd.notna(x) else ""
    )

# ================================
# 7. Eliminar columna CATEGORIA (sin afectar subtotales)
# ================================
if "CATEGORIA" in df_final.columns:
    df_final = df_final.drop(columns=["CATEGORIA"])

# ================================
# 8. Exportar a Excel sin formato
# ================================
df_final.to_excel(EXCEL_SALIDA, index=False)

# ================================
# 9. Dar formato con openpyxl
# ================================
wb = openpyxl.load_workbook(EXCEL_SALIDA)
ws = wb.active

# ---- Estilos ----
header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
subtotal_font = Font(bold=True, color="1F4E78")
subtotal_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
thin_border = Border(
    left=Side(style="thin", color="AAAAAA"),
    right=Side(style="thin", color="AAAAAA"),
    top=Side(style="thin", color="AAAAAA"),
    bottom=Side(style="thin", color="AAAAAA"),
)

# ---- Encabezados ----
for cell in ws[1]:
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

# ---- Celdas ----
for row in ws.iter_rows(min_row=2):
    for cell in row:
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

        # Columnas numéricas con formato 2 decimales
        if cell.column_letter in ["F", "G", "H"]:  # IMPORTE, IVA, TOTAL
            cell.number_format = numbers.FORMAT_NUMBER_00
            cell.alignment = Alignment(horizontal="right", vertical="center")

        # Subtotales
        if cell.column_letter == "E" and cell.value is not None:
            if str(cell.value).startswith("SUBTOTAL"):
                for c in ws[cell.row]:
                    c.font = subtotal_font
                    c.fill = subtotal_fill
                    c.border = thin_border

# ---- Ajustar ancho de columnas automáticamente
for col in ws.columns:
    max_length = 0
    col_letter = col[0].column_letter
    for cell in col:
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))
    ws.column_dimensions[col_letter].width = max_length + 2

# ---- Guardar Excel final
wb.save(EXCEL_SALIDA)
print(f"Facturas_Organizadas.xlsx creado con éxito en: {EXCEL_SALIDA}")
