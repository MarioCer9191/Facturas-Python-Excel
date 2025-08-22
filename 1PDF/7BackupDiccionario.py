import os
import json

# ================================
# Rutas
# ================================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Carpeta Facturas
TXT_ENTRADA = os.path.join(RAIZ, "Categorias.txt")
JSON_BACKUP = os.path.join(RAIZ, "categorias_backup.json")

# ================================
# Leer Categorias.txt
# ================================
def leer_categorias_txt():
    diccionario = {}
    if not os.path.exists(TXT_ENTRADA):
        print(f"No se encontró el archivo {TXT_ENTRADA}")
        return diccionario

    with open(TXT_ENTRADA, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or ":" not in linea or linea.startswith("#"):
                continue
            cat, palabras = linea.split(":", 1)
            diccionario[cat.strip()] = [p.strip() for p in palabras.split(",")]
    return diccionario

# ================================
# Leer backup previo (si existe)
# ================================
def leer_backup_json():
    if not os.path.exists(JSON_BACKUP):
        return {}
    with open(JSON_BACKUP, "r", encoding="utf-8") as f:
        return json.load(f)

# ================================
# Fusionar diccionarios
# ================================
def fusionar_diccionarios(original, nuevo):
    for cat, palabras in nuevo.items():
        if cat in original:
            # Evitar duplicados
            palabras_existentes = set(original[cat])
            for p in palabras:
                if p not in palabras_existentes:
                    original[cat].append(p)
        else:
            original[cat] = palabras
    return original

# ================================
# Guardar backup
# ================================
def guardar_backup(diccionario):
    with open(JSON_BACKUP, "w", encoding="utf-8") as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=4)
    print(f"Backup actualizado en {JSON_BACKUP}")

# ================================
# Ejecución
# ================================
if __name__ == "__main__":
    categorias_txt = leer_categorias_txt()
    backup_prev = leer_backup_json()
    backup_actualizado = fusionar_diccionarios(backup_prev, categorias_txt)
    guardar_backup(backup_actualizado)
