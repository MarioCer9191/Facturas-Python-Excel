# PDF.py
# Coordinador del departamento 1PDF: ejecuta todos los scripts de la carpeta 1PDF

import os
import subprocess

# Carpeta donde están los scripts de PDF
carpeta_scripts = os.path.join(os.path.dirname(__file__), "1PDF")

# Listamos todos los archivos .py dentro de 1PDF y los ordenamos alfabéticamente
scripts = sorted([f for f in os.listdir(carpeta_scripts) if f.endswith(".py")])

# Ejecutamos cada script en orden
for script in scripts:
    ruta_script = os.path.join(carpeta_scripts, script)
    print(f"=== Ejecutando {script} ===")
    subprocess.run(["python", ruta_script], check=True)
    print(f"=== {script} finalizado ===")
