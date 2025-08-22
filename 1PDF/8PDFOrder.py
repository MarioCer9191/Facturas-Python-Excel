import os
import pandas as pd

# ================================
# Configuración de rutas
# ================================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_ENTRADA = os.path.join(RAIZ, "1PDF", "PDFCategory_Final.csv")
CSV_SALIDA = os.path.join(RAIZ, "1PDF", "PDFOrder.csv")

# ================================
# Main
# ================================
def main():
    # Leer solo las columnas necesarias
    df = pd.read_csv(CSV_ENTRADA, usecols=["FacturaID", "Categoria"], dtype=str)

    # Guardar en PDFOrder.csv
    df.to_csv(CSV_SALIDA, index=False, encoding="utf-8")
    print(f"Archivo generado: {CSV_SALIDA}")

if __name__ == "__main__":
    main()
