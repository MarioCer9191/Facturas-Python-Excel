import os
import re
import shutil

# ============================
# Definir rutas
# ============================
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
carpeta_facturas = os.path.join(RAIZ, "AgregarFacturas")
carpeta_ignorados = os.path.join(carpeta_facturas, "IGNORADOS")

# ============================
# Crear carpeta IGNORADOS si no existe
# ============================
if not os.path.exists(carpeta_ignorados):
    os.makedirs(carpeta_ignorados)
    print(f"Carpeta creada: {carpeta_ignorados}")
else:
    print(f"La carpeta ya existe: {carpeta_ignorados}")

# ============================
# Expresión regular para UUID
# ============================
uuid_regex = re.compile(r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}")

# ============================
# Iterar sobre archivos PDF
# ============================
for root, dirs, files in os.walk(carpeta_facturas):
    for file in files:
        if file.lower().endswith(".pdf"):
            ruta_completa = os.path.join(root, file)
            try:
                # Verificar si el nombre contiene un UUID
                if not uuid_regex.search(file):
                    # Mover archivo a carpeta IGNORADOS
                    destino = os.path.join(carpeta_ignorados, file)
                    
                    # Evitar sobrescribir archivos con mismo nombre
                    if os.path.exists(destino):
                        base, ext = os.path.splitext(file)
                        contador = 1
                        while os.path.exists(destino):
                            destino = os.path.join(carpeta_ignorados, f"{base}_{contador}{ext}")
                            contador += 1
                    
                    shutil.move(ruta_completa, destino)
                    print(f"Archivo movido a IGNORADOS: {file}")
                else:
                    # Archivo válido, no hacer nada
                    print(f"Archivo válido, se mantiene: {file}")
            except Exception as e:
                print(f"No se pudo procesar {file}: {e}")
