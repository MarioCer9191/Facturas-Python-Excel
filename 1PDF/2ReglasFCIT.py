import os

# Carpeta raíz
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Archivos
ARCHIVO_REGLAS = os.path.join(RAIZ, "ReglasPersonalizadas.txt")
CARPETA_FCIT = os.path.join(RAIZ, "2FCIT")
ARCHIVO_FCIT = os.path.join(CARPETA_FCIT, "FCIT.txt")
CARPETA_1PDF = os.path.join(RAIZ, "1PDF")
ARCHIVO_KEYWORDS = os.path.join(CARPETA_1PDF, "KeyWords.txt")


def crear_archivo_reglas():
    """Crea ReglaPersonalizadas.txt en la raíz si no existe"""
    if not os.path.exists(ARCHIVO_REGLAS):
        with open(ARCHIVO_REGLAS, "w", encoding="utf-8") as f:
            f.write(
                "Cada línea define cómo un CONCEPTO se asigna a un CONJUNTO.\n"
                "Formato: \"Concepto exacto\" -> \"Conjunto deseado\"\n\n"
                "\"ANDREA MICHELLE ESCOBEDO GALLARDO\" -> \"COLEGIATURAS\"\n"
                "\"NACIONAL DE COMBUSTIBLES Y COMBUSTIBLES\" -> \"GASOLINA\"\n"
                "\"CONCESIONARIA ASM\" -> \"CONCESIONARIA\"\n"
                "\"FONDO NACIONAL DE INFRAESTRUCTURA\" -> \"FONDO\"\n"
            )
        print(f"Archivo de reglas creado en: {ARCHIVO_REGLAS}")
    else:
        print(f"Archivo de reglas existente encontrado: {ARCHIVO_REGLAS}")


def crear_archivo_fcit():
    """Crea FCIT.txt dentro de la carpeta 2FCIT si no existe"""
    os.makedirs(CARPETA_FCIT, exist_ok=True)
    if not os.path.exists(ARCHIVO_FCIT):
        with open(ARCHIVO_FCIT, "w", encoding="utf-8") as f:
            f.write(
                "Cada línea define cómo un CONCEPTO se asigna a un CONJUNTO.\n"
                "Formato: \"Concepto exacto\" -> \"Conjunto deseado\"\n\n"
                "\"ANDREA MICHELLE ESCOBEDO GALLARDO\" -> \"COLEGIATURAS\"\n"
                "\"NACIONAL DE COMBUSTIBLES Y COMBUSTIBLES\" -> \"GASOLINA\"\n"
            )
        print(f"Archivo FCIT.txt creado en: {ARCHIVO_FCIT}")
    else:
        print(f"Archivo FCIT.txt existente encontrado: {ARCHIVO_FCIT}")


def crear_archivo_keywords():
    """Crea KeyWords.txt dentro de 1PDF con instrucciones si no existe"""
    os.makedirs(CARPETA_1PDF, exist_ok=True)
    if not os.path.exists(ARCHIVO_KEYWORDS):
        with open(ARCHIVO_KEYWORDS, "w", encoding="utf-8") as f:
            f.write(
                "# Define palabras clave para identificar categorías en las facturas.\n"
                "# Formato: palabra = CATEGORIA\n"
                "# Ejemplos:\n"
                "peaje = CASETAS\n"
                "autopista = CASETAS\n"
                "gasolina = GASOLINA\n"
                "diesel = GASOLINA\n"
                "hotel = HOSPEDAJE\n"
                "vuelo = TRANSPORTE AÉREO\n\n"
                "# Notas importantes:\n"
                "# - No distingue mayúsculas/minúsculas.\n"
                "# - Puedes usar varias palabras para la misma categoría.\n"
                "# - No dejes espacios antes del signo '='.\n"
            )
        print(f"Archivo KeyWords.txt creado en: {ARCHIVO_KEYWORDS}")
    else:
        print(f"Archivo KeyWords.txt existente encontrado: {ARCHIVO_KEYWORDS}")


if __name__ == "__main__":
    crear_archivo_reglas()
    crear_archivo_fcit()
    crear_archivo_keywords()
