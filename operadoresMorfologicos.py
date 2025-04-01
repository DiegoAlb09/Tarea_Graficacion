import cv2
import numpy as np
import os
from skimage.morphology import skeletonize

def aplicar_operadores_morfologicos(imagen):
    kernel = np.ones((3,3), np.uint8)  # Kernel 3x3 para operaciones
    
    apertura = cv2.morphologyEx(imagen, cv2.MORPH_OPEN, kernel)  # Quitar ruido
    cierre = cv2.morphologyEx(imagen, cv2.MORPH_CLOSE, kernel)  # Suavizar bordes
    dilatacion = cv2.dilate(imagen, kernel, iterations=2)  # Rellenar huecos
    
    # Esqueletización usando skimage.morphology
    # Convertir a formato binario (True/False) requerido por skimage
    imagen_binaria = imagen > 0
    esqueleto = skeletonize(imagen_binaria)
    # Convertir de vuelta a formato uint8 para OpenCV
    esqueleto = (esqueleto * 255).astype(np.uint8)
    
    return apertura, cierre, dilatacion, esqueleto

def guardar_imagenes(nombre, apertura, cierre, dilatacion, esqueleto):
    directorios = {
        'Imagenes_apertura': (apertura, "_apertura"),
        'Imagenes_cierre': (cierre, "_cierre"),
        'Imagenes_dilatacion': (dilatacion, "_dilatacion"),
        'Imagenes_esqueleto': (esqueleto, "_esqueleto")
    }
    
    base_nombre = os.path.splitext(nombre)[0]  # Obtener nombre sin extensión
    
    for carpeta, (imagen, sufijo) in directorios.items():
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        nombre_archivo = f"{base_nombre}{sufijo}.png"
        cv2.imwrite(os.path.join(carpeta, nombre_archivo), imagen)

def procesar_imagenes(carpeta_entrada):
    archivos = os.listdir(carpeta_entrada)
    for archivo in archivos:
        ruta = os.path.join(carpeta_entrada, archivo)
        imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
        
        if imagen is None:
            print(f"No se pudo cargar la imagen: {archivo}")
            continue
        
        apertura, cierre, dilatacion, esqueleto = aplicar_operadores_morfologicos(imagen)
        guardar_imagenes(archivo, apertura, cierre, dilatacion, esqueleto)
        
        print(f"Procesado: {archivo}")

# Ejecutar procesamiento
procesar_imagenes('Imagenes_binarias')
