# Run.py
import os
import subprocess
import time
from tqdm import tqdm

# ============================
# Introducción
# ============================
intro = """
📌 Hola! Esta es una herramienta que organizará todos tus PDFs por Categoría
y creará un Excel con toda la información ya organizada. 

⏳ Espera mientras hacemos el trabajo pesado.

Que tengas un buen día y gracias por usar esta herramienta que con mucho esfuerzo 
y dedicación pude lograr. 😊
"""
print(intro)
time.sleep(2)

agradecimiento = """
🎓 Gracias al Lic. Roberto Cervantes Mendoza,
por ser mi mentor en la Contaduría y un Excelente Padre.

Usuario, sé paciente, ten un buen día.
Gracias por utilizar 'Herramienta de Organización y Gestión de Facturas'. 🛠️
MCervantes9191 - Derechos Reservados (c)
"""
print(agradecimiento)
time.sleep(3)

# ============================
# Carpetas y scripts
# ============================
carpetas = [
    ("1PDF", "Ejecutando scripts de 1PDF..."),
    ("2FCIT", "Ejecutando scripts de 2FCIT..."),
    ("3EXCEL", "Ejecutando scripts de 3EXCEL...")
]

RAIZ = os.path.dirname(__file__)

for carpeta, mensaje in carpetas:
    carpeta_path = os.path.join(RAIZ, carpeta)
    print(f"\n📂 {mensaje}")
    
    # Listar scripts en orden numérico
    scripts = [f for f in os.listdir(carpeta_path) if f.endswith(".py")]
    
    def obtener_numero(nombre):
        numero = ''
        for c in nombre:
            if c.isdigit():
                numero += c
            else:
                break
        return int(numero) if numero else 0
    
    scripts.sort(key=obtener_numero)
    
    for script in tqdm(scripts, desc=f"Procesando {carpeta}", ncols=100, unit="script"):
        ruta_script = os.path.join(carpeta_path, script)
        try:
            subprocess.run(["python", ruta_script], check=True)
        except subprocess.CalledProcessError:
            print(f"❌ Error al ejecutar {script}, revisa el script para más detalles.")
            continue
        time.sleep(0.2)

print("\n✅ Todos los scripts ejecutados. ¡Proceso finalizado con éxito! 🎉")
