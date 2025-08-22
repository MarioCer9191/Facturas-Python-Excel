import os
import pandas as pd

# ================================
# Configuración de rutas
# ================================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_ENTRADA = os.path.join(RAIZ, "1PDF", "PDFOrder.csv")
CARPETA_DESTINO = os.path.join(RAIZ, "Facturas_Ordenadas")

# ================================
# Crear carpeta si no existe
# ================================
def asegurar_carpeta(ruta):
    if not os.path.exists(ruta):
        os.makedirs(ruta)

# ================================
# Main
# ================================
def main():
    # Crear carpeta principal si no existe
    asegurar_carpeta(CARPETA_DESTINO)

    # Leer CSV usando solo la columna Categoria
    df = pd.read_csv(CSV_ENTRADA, usecols=["Categoria"], dtype=str)

    # Obtener categorías únicas
    categorias_unicas = df["Categoria"].dropna().str.strip().unique()

    for categoria in categorias_unicas:
        if not categoria:
            categoria = "SIN_CATEGORIA"
        ruta_categoria = os.path.join(CARPETA_DESTINO, categoria)
        asegurar_carpeta(ruta_categoria)
        print(f"Carpeta creada: {ruta_categoria}")

    print("Proceso finalizado. Todas las carpetas de categorías están listas.")

if __name__ == "__main__":
    main()
