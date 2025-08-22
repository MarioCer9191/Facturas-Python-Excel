# 🧾 Proyecto Facturas Python-Excel

Este proyecto automatiza el **procesamiento de facturas en PDF** para extraer información clave (Fecha, Folio, RFC, Concepto, Importe, IVA y Total) y generar un archivo final en **Excel** con todos los datos organizados.

## 🚀 Características

- Escanea y organiza facturas en PDF en carpetas por categorías (Gasolinas, Teléfonos, IMSS, etc.).
- Extrae automáticamente datos fiscales relevantes.
- Consolida los resultados en un archivo Excel listo para contabilidad.
- Modularidad en tres fases principales:
  1. **1PDF/** → Lectura, orden y preprocesamiento de PDFs.
  2. **2FCIT/** → Extracción de campos clave de facturas.
  3. **3EXCEL/** → Generación del archivo Excel final.
- Archivo principal: `RUN.py` para ejecutar todo el flujo.

## 📂 Estructura del proyecto

├── RUN.py # Script principal que ejecuta todo el proceso
├── 1PDF.py # Entrada a la etapa de procesamiento de PDFs
├── 2FCIT.py # Entrada a la etapa de extracción de campos
├── 3EXCEL.py # Entrada a la generación de Excel
├── categorias_backup.json # Diccionario de categorías de facturas
├── 1PDF/ # Scripts de procesamiento de PDFs
├── 2FCIT/ # Scripts de extracción de datos fiscales
├── 3EXCEL/ # Scripts de salida en Excel
├── Facturas_Ordenadas/ # Carpeta con facturas clasificadas (IGNORADA en Git)
└── Agregar paquete de facturas/ # Carpeta de facturas entrantes (IGNORADA en Git)


## ⚙️ Requisitos

- Python 3.9+  
- Bibliotecas recomendadas:
  - `pandas`
  - `openpyxl`
  - `PyPDF2`
  - `re` (expresiones regulares, incluida en la librería estándar)

## Instalación rápida:

```bash
pip install pandas openpyxl PyPDF2

▶️ Uso

Coloca las facturas en la carpeta Agregar paquete de facturas.

Ejecuta el flujo completo con:

python RUN.py


El resultado final será un archivo Excel con todas las facturas organizadas.

📝 Notas

Puedes modificar el archivo categorias_backup.json para actualizar o añadir categorías personalizadas.

✍️ Proyecto creado para simplificar la gestión contable y ahorrar horas de trabajo manual.

