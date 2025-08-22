import os
import shutil

# ================================
# Configuración de rutas
# ================================
import os

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_ORIGEN = os.path.join(RAIZ, "Agregar paquete de facturas")
CARPETA_DESTINO = os.path.join(RAIZ, "Facturas_Ordenadas")
LOG_FALTANTES = os.path.join(RAIZ, "PDFs_no_moved.txt")

# ================================
# Crear carpeta destino si no existe
# ================================
def asegurar_carpeta(ruta):
    if not os.path.exists(ruta):
        os.makedirs(ruta)

# ================================
# Main
# ================================
def main():
    asegurar_carpeta(CARPETA_DESTINO)
    pdfs_faltantes = []

    for archivo in os.listdir(CARPETA_ORIGEN):
        if archivo.lower().endswith(".pdf"):
            ruta_origen = os.path.join(CARPETA_ORIGEN, archivo)
            ruta_destino = os.path.join(CARPETA_DESTINO, archivo)
            try:
                shutil.move(ruta_origen, ruta_destino)
            except Exception as e:
                print(f"No se pudo mover {archivo}: {e}")
                pdfs_faltantes.append(archivo)

    # Guardar log de PDFs que no se movieron
    if pdfs_faltantes:
        with open(LOG_FALTANTES, "w", encoding="utf-8") as f:
            for item in pdfs_faltantes:
                f.write(f"{item}\n")
        print(f"Se generó log de PDFs no movidos en: {LOG_FALTANTES}")

    print("Todos los PDFs han sido procesados.")

if __name__ == "__main__":
    main()
