import os
import shutil
import json
import xml.etree.ElementTree as ET

# Rutas
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_FACTURAS = os.path.join(RAIZ, "AgregarFacturas")
RUTA_JSON_CATALOGO = os.path.join(RAIZ, "1PDF", "CATALOGO.json")

# Cargar catálogo clave_producto -> descripcion (categoria)
with open(RUTA_JSON_CATALOGO, "r", encoding="utf-8") as f:
    catalogo = json.load(f)
clave_categoria = {str(item["clave_producto"]): item["descripcion"] for item in catalogo if "clave_producto" in item and "descripcion" in item}

# Procesar cada archivo XML en la carpeta
for archivo in os.listdir(CARPETA_FACTURAS):
    if archivo.lower().endswith(".xml"):
        ruta_xml = os.path.join(CARPETA_FACTURAS, archivo)
        try:
            tree = ET.parse(ruta_xml)
            root = tree.getroot()
            # Buscar el atributo ObjetoImpuesto en el nodo raíz o en los nodos hijos
            objeto_impuesto = root.attrib.get("ObjetoImpuesto", "")
            if not objeto_impuesto:
                for elem in root.iter():
                    if "ObjetoImpuesto" in elem.attrib:
                        objeto_impuesto = elem.attrib["ObjetoImpuesto"]
                        break
            categoria = clave_categoria.get(str(objeto_impuesto), None)
            if categoria:
                carpeta_destino = os.path.join(CARPETA_FACTURAS, categoria)
                if not os.path.exists(carpeta_destino):
                    os.makedirs(carpeta_destino)
                shutil.move(ruta_xml, os.path.join(carpeta_destino, archivo))
                print(f"Movido: {archivo} → {carpeta_destino}")
                uuid = archivo.split(".")[0]
                pdf_name = f"{uuid}.PDF"
                ruta_pdf = os.path.join(CARPETA_FACTURAS, pdf_name)
                if os.path.exists(ruta_pdf):
                    shutil.move(ruta_pdf, os.path.join(carpeta_destino, pdf_name))
                    print(f"Movido: {pdf_name} → {carpeta_destino}")
                else:
                    print(f"⚠ No se encontró PDF para: {uuid}")
            else:
                print(f"⚠ No se encontró categoría para: {archivo} (ObjetoImpuesto: {objeto_impuesto})")
        except Exception as e:
            print(f"❌ Error procesando {archivo}: {e}")

# Eliminar todos los archivos .json y .txt en la carpeta AgregarFacturas y sus subcarpetas
for root_dir, dirs, files in os.walk(CARPETA_FACTURAS):
    for file in files:
        if file.lower().endswith(".json") or file.lower().endswith(".txt"):
            ruta_archivo = os.path.join(root_dir, file)
            try:
                os.remove(ruta_archivo)
                print(f"Eliminado: {ruta_archivo}")
            except Exception as e:
                print(f"❌ Error eliminando {ruta_archivo}: {e}")

print("✅ Archivos XML y PDF organizados por categoría y archivos .json/.txt eliminados.")