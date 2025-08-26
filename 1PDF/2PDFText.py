# 4PdfATxt.py
import os
import fitz  # PyMuPDF

# ================================
# Configuración
# ================================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_FACTURAS = os.path.join(RAIZ, "AgregarFacturas")

def pdf_a_txt(ruta_pdf, ruta_txt):
    try:
        doc = fitz.open(ruta_pdf)
        texto_completo = ""

        for pagina in doc:
            texto_completo += pagina.get_text("text") + " "

        # ================================
        # Eliminar saltos de línea originales
        # ================================
        texto_completo = texto_completo.replace("\r", " ").replace("\n", " ")

        # ================================
        # Insertar salto de línea en lugar de cada espacio
        # ================================
        texto_formateado = texto_completo.replace(" ", "\n")

        # ================================
        # Añadir nombre del archivo al inicio
        # ================================
        nombre_archivo = os.path.basename(ruta_txt)
        texto_formateado = f"Archivo: {nombre_archivo}\n" + texto_formateado

        # Guardar en archivo txt
        with open(ruta_txt, "w", encoding="utf-8") as f:
            f.write(texto_formateado)

        print(f"✔ Texto extraído: {ruta_txt}")

    except Exception as e:
        print(f" Error con {ruta_pdf}: {e}")


def main():
    if not os.path.exists(CARPETA_FACTURAS):
        print(f"⚠ No existe la carpeta: {CARPETA_FACTURAS}")
        return

    for file in os.listdir(CARPETA_FACTURAS):
        if file.lower().endswith(".pdf"):
            ruta_pdf = os.path.join(CARPETA_FACTURAS, file)
            nombre_base, _ = os.path.splitext(file)
            ruta_txt = os.path.join(CARPETA_FACTURAS, f"{nombre_base}.txt")

            pdf_a_txt(ruta_pdf, ruta_txt)


if __name__ == "__main__":
    main()
