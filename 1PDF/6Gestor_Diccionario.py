import os
import json

# RAIZ = carpeta padre de 1PDF (Facturas)
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  
TXT_FILE = os.path.join(RAIZ, "Categorias.txt")  # Archivo en la raíz Facturas
BACKUP_FILE = os.path.join(RAIZ, "categorias_backup.json")  # Backup en la raíz también

# Contenido inicial del archivo Categorias.txt
CONTENIDO_INICIAL = """# Archivo de categorías para el proyecto de facturas
# Cada línea representa una categoría.
# Las palabras clave se separan por comas.
# El usuario puede agregar nuevas categorías o palabras clave sin tocar el código.
# Ejemplo:
CASETAS: PEAJE
GASOLINAS: GASOLINA, PEMEX, COMBUSTIBLE
"""

def crear_txt_instrucciones():
    os.makedirs(RAIZ, exist_ok=True)
    if not os.path.exists(TXT_FILE):
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write(CONTENIDO_INICIAL)
        print(f" Se creó el archivo de instrucciones {TXT_FILE}")
    else:
        print(f"ℹ El archivo {TXT_FILE} ya existe")

def cargar_diccionario():
    diccionario = {}
    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea or ":" not in linea or linea.startswith("#"):
                    continue
                cat, palabras = linea.split(":", 1)
                diccionario[cat.strip().upper()] = [p.strip().upper() for p in palabras.split(",")]
    elif os.path.exists(BACKUP_FILE):
        print(" Categorias.txt no encontrado. Cargando desde backup...")
        with open(BACKUP_FILE, "r", encoding="utf-8") as f:
            diccionario = json.load(f)
    else:
        print(" No se encontró Categorias.txt ni backup. Se creará un diccionario vacío.")
    return diccionario

def guardar_backup(diccionario):
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(diccionario, f, indent=4, ensure_ascii=False)

def agregar_categoria(diccionario, categoria, palabras):
    categoria = categoria.strip().upper()
    palabras = [p.strip().upper() for p in palabras]
    if categoria in diccionario:
        diccionario[categoria] = list(set(diccionario[categoria] + palabras))
    else:
        diccionario[categoria] = palabras
    guardar_backup(diccionario)

def main():
    crear_txt_instrucciones()
    diccionario = cargar_diccionario()
    print("Diccionario cargado:", diccionario)

if __name__ == "__main__":
    main()
