import os
import glob
from PyPDF2 import PdfFileReader

# Función para convertir un archivo PDF a texto
def convertir_a_texto(archivo_pdf):
    try:
        with open(archivo_pdf, 'rb') as f:
            pdf = PdfFileReader(f)
            texto = ''
            for pagina in range(pdf.getNumPages()):
                try:
                    texto += pdf.getPage(pagina).extractText()
                except UnicodeDecodeError:
                    # En caso de error de codificación, intenta decodificar con Latin-1 (ISO-8859-1)
                    try:
                        texto += pdf.getPage(pagina).extractText(encoding='ISO-8859-1')
                    except:
                        # Si aún hay un error, salta el archivo y continúa con el siguiente
                        print("Salta archivo " + archivo_pdf)
                        return None
            return texto
    except UnicodeDecodeError:
        # En caso de error de decodificación en el archivo no PDF, imprime un mensaje y continúa con el siguiente archivo
        print("Error decodificacion " + archivo_pdf)
        return None

# Ruta de la carpeta A
carpeta_a = 'D:\\'

# Ruta de la carpeta B
carpeta_b = 'F:\\PDFTXT'

# Recorre la carpeta A y todas sus subcarpetas
for ruta_actual, subcarpetas, archivos in os.walk(carpeta_a):
    # Crea la ruta correspondiente en la carpeta B
    ruta_b = os.path.join(carpeta_b, os.path.relpath(ruta_actual, carpeta_a))
    os.makedirs(ruta_b, exist_ok=True)
    
    # Recorre los archivos de la carpeta actual
    for archivo in archivos:
        # Verifica si el archivo es de tipo PDF
        if archivo.lower().endswith('.pdf'):
            # Ruta completa del archivo en la carpeta A
            ruta_archivo_a = os.path.join(ruta_actual, archivo)
            
            # Ruta completa del archivo convertido en la carpeta B
            ruta_archivo_b = os.path.join(ruta_b, archivo.replace('.pdf', '.txt'))
            
            # Convierte el archivo PDF a texto y lo guarda en la carpeta B
            texto = convertir_a_texto(ruta_archivo_a)
            with open(ruta_archivo_b, 'w', encoding='utf-8') as f:
                f.write(texto)
                print(ruta_archivo_b)
