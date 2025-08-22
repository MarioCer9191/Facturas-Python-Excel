import os
import subprocess

def ejecutar_scripts_fcit():
    carpeta_fcit = "2FCIT"
    
    # Solo listamos archivos .py y excluimos 2FCIT.py mismo
    scripts = [f for f in os.listdir(carpeta_fcit) 
               if f.lower().endswith(".py") and f != "2FCIT.py"]
    
    # Ordenamos por número al inicio del nombre
    def obtener_numero(nombre):
        # Toma los dígitos al inicio del archivo antes del primer carácter no numérico
        numero = ''
        for c in nombre:
            if c.isdigit():
                numero += c
            else:
                break
        return int(numero)
    
    scripts = sorted(scripts, key=obtener_numero)
    
    # Ejecutamos cada script
    for script in scripts:
        ruta_script = os.path.join(carpeta_fcit, script)
        print(f"Ejecutando: {script}")
        subprocess.run(["python", ruta_script], check=True)

if __name__ == "__main__":
    ejecutar_scripts_fcit()
