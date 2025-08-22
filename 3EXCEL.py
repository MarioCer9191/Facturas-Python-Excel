# 3EXCEL.py
import os
import subprocess
import sys

# Carpeta donde están los scripts de Excel
CARPETA_EXCEL = os.path.join(os.path.dirname(__file__), "3EXCEL")

def ejecutar_scripts():
    if not os.path.exists(CARPETA_EXCEL):
        print(f"❌ La carpeta {CARPETA_EXCEL} no existe")
        return

    # Lista todos los .py en la carpeta, excluyendo archivos no numéricos
    scripts = [f for f in os.listdir(CARPETA_EXCEL) 
               if f.endswith(".py")]

    # Función para obtener el número al inicio del archivo
    def obtener_numero(nombre):
        numero = ''
        for c in nombre:
            if c.isdigit():
                numero += c
            else:
                break
        return int(numero) if numero else 0

    # Ordenar los scripts por el número inicial
    scripts.sort(key=obtener_numero)

    print(f"Se encontraron {len(scripts)} scripts para ejecutar en orden numérico:")
    for script in scripts:
        print(f"Ejecutando {script}...")
        ruta_script = os.path.join(CARPETA_EXCEL, script)
        resultado = subprocess.run([sys.executable, ruta_script], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{script} ejecutado correctamente.\n")
        else:
            print(f"❌ Error al ejecutar {script}:\n{resultado.stderr}\n")

if __name__ == "__main__":
    ejecutar_scripts()
