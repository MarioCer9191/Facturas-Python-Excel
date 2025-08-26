import os
import json

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JSON_PATH = os.path.join(RAIZ, "1PDF", "CATALOGO.json")
TXT_PATH = os.path.join(RAIZ, "CATEGORIAS.txt")

# Si el archivo personalizados.txt no existe, lo crea con instrucciones y ejemplo
if not os.path.exists(TXT_PATH):
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        f.write(
            "# INSTRUCCIONES:\n"
            "# Añade tus datos en cada línea siguiendo el formato:\n"
            "# descripcion|clave_producto|descripcion_producto|clave_unidad|descripcion_unidad\n"
            "# Ejemplo:\n"
            "EJEMPLO DE SERVICIO|00000000|EJEMPLO PRODUCTO|EJ|EJEMPLO UNIDAD\n"
            "# Puedes copiar la línea de ejemplo y modificar los valores.\n"
            "# No borres la primera línea de instrucciones.\n"
            "# También puedes usar la siguiente línea como plantilla:\n"
            "DESCRIPCION|CLAVE_PRODUCTO|DESCRIPCION_PRODUCTO|CLAVE_UNIDAD|DESCRIPCION_UNIDAD\n"
        )
    print("Archivo personalizados.txt creado con instrucciones. Agrega tus datos en formato:\ndescripcion|clave_producto|descripcion_producto|clave_unidad|descripcion_unidad")

# Carga el JSON existente
if os.path.exists(JSON_PATH):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        datos_json = json.load(f)
else:
    datos_json = []

# Elimina bloques repetidos, conservando el más actual (última aparición)
bloques_unicos = {}
for item in datos_json:
    clave = (
        item.get("descripcion", ""),
        item.get("clave_producto", ""),
        item.get("descripcion_producto", ""),
        item.get("clave_unidad", ""),
        item.get("descripcion_unidad", "")
    )
    bloques_unicos[clave] = item  # Si hay repetidos, el último sobrescribe al anterior

datos_json = list(bloques_unicos.values())

# Guarda el estado inicial para comparar después
datos_json_inicial = datos_json.copy()

# Lee los datos personalizados del txt y los agrega al JSON
with open(TXT_PATH, "r", encoding="utf-8") as f:
    for linea in f:
        if "|" in linea and not linea.strip().startswith("#"):
            partes = [x.strip().upper() for x in linea.strip().split("|")]
            while len(partes) < 5:
                partes.append("")
            datos_json.append({
                "descripcion": partes[0],
                "clave_producto": partes[1],
                "descripcion_producto": partes[2],
                "clave_unidad": partes[3],
                "descripcion_unidad": partes[4]
            })

# Elimina los ejemplos del JSON si existen
datos_json = [
    item for item in datos_json
    if not (
        (item["descripcion"] == "EJEMPLO DE SERVICIO" and
         item["clave_producto"] == "00000000" and
         item["descripcion_producto"] == "EJEMPLO PRODUCTO" and
         item["clave_unidad"] == "EJ" and
         item["descripcion_unidad"] == "EJEMPLO UNIDAD")
        or
        (item["descripcion"] == "DESCRIPCION" and
         item["clave_producto"] == "CLAVE_PRODUCTO" and
         item["descripcion_producto"] == "DESCRIPCION_PRODUCTO" and
         item["clave_unidad"] == "CLAVE_UNIDAD" and
         item["descripcion_unidad"] == "DESCRIPCION_UNIDAD")
    )
]

# Determina qué elementos fueron añadidos
añadidos = [
    item for item in datos_json
    if item not in datos_json_inicial
]

# Guarda el JSON actualizado en la carpeta raíz "Facturas"
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(datos_json, f, ensure_ascii=False, indent=4)

if añadidos:
    print("Se añadieron al JSON los siguientes elementos:")
    for item in añadidos:
        print(item)
else:
    print("No se añadieron nuevos elementos al JSON.")

print("¡Datos personalizados agregados y JSON actualizado correctamente!")