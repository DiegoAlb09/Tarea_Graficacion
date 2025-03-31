import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

def calcular_centro_masa(imagen_binaria):
    """Calcula el centro de masa de una imagen binaria"""
    momentos = cv2.moments(imagen_binaria)
    if momentos['m00'] != 0:
        cx = int(momentos['m10'] / momentos['m00'])
        cy = int(momentos['m01'] / momentos['m00'])
        return cx, cy
    return None, None

def calcular_momentos_hu(imagen_binaria):
    """Calcula los momentos de Hu para una imagen binaria"""
    momentos = cv2.moments(imagen_binaria)
    momentos_hu = cv2.HuMoments(momentos).flatten()
    return momentos_hu

def rotar_imagen(imagen, angulo):
    """
    Rota la imagen alrededor de su centro de masa
    Usa interpolación bilineal y maneja bordes
    """
    # Obtener centro de masa
    xcm, ycm = calcular_centro_masa(imagen)
    
    # Matriz de rotación
    alto, ancho = imagen.shape[:2]
    matriz_rotacion = cv2.getRotationMatrix2D((xcm, ycm), angulo, 1)
    
    # Rotar imagen con interpolación bilineal
    imagen_rotada = cv2.warpAffine(
        imagen, 
        matriz_rotacion, 
        (ancho, alto), 
        flags=cv2.INTER_LINEAR,  # Interpolación bilineal
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0  # Fondo negro
    )
    
    return imagen_rotada

def rellenar_huecos(imagen):
    """
    Rellena huecos en imagen binaria usando operadores morfológicos
    """
    # Kernel para operaciones morfológicas
    kernel = np.ones((3,3), np.uint8)
    
    # Cierre morfológico: dilatar seguido de erosión
    imagen_cerrada = cv2.morphologyEx(
        imagen, 
        cv2.MORPH_CLOSE, 
        kernel, 
        iterations=2
    )
    
    # Relleno de huecos internos
    imagen_rellena = imagen_cerrada.copy()
    cv2.floodFill(imagen_rellena, None, (0,0), 255)
    imagen_rellena = cv2.bitwise_not(imagen_rellena)
    
    return imagen_rellena

def procesar_imagenes(directorio):
    # Crear directorios de resultados
    os.makedirs('rotaciones', exist_ok=True)
    os.makedirs('resultados', exist_ok=True)
    
    # Ángulos de rotación
    angulos = [0, 45, 135]
    
    # Almacenar resultados
    resultados = []
    
    # Procesar cada imagen
    for archivo in os.listdir(directorio):
        if not archivo.endswith('.png'):
            continue
        
        ruta = os.path.join(directorio, archivo)
        imagen_original = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
        
        # Binarizar
        _, imagen_binaria = cv2.threshold(imagen_original, 127, 255, cv2.THRESH_BINARY)
        
        # Momentos Hu originales
        momentos_originales = calcular_momentos_hu(imagen_binaria)
        
        # Procesar cada ángulo
        for angulo in angulos:
            # Rotar imagen
            imagen_rotada = rotar_imagen(imagen_binaria, angulo)
            
            # Rellenar huecos
            imagen_rellena = rellenar_huecos(imagen_rotada)
            
            # Calcular momentos Hu
            momentos_rotados = calcular_momentos_hu(imagen_rellena)
            
            # Guardar imagen rotada
            plt.figure(figsize=(10,5))
            plt.subplot(121)
            plt.title(f'Original: {archivo}')
            plt.imshow(imagen_binaria, cmap='gray')
            plt.subplot(122)
            plt.title(f'Rotada {angulo}°')
            plt.imshow(imagen_rellena, cmap='gray')
            plt.tight_layout()
            plt.savefig(f'rotaciones/{archivo}_rotacion_{angulo}.png')
            plt.close()
            
            # Almacenar resultados
            fila = {
                'Imagen': archivo,
                'Ángulo': angulo,
                'Hu1 Original': momentos_originales[0],
                'Hu2 Original': momentos_originales[1],
                'Hu3 Original': momentos_originales[2],
                'Hu1 Rotado': momentos_rotados[0],
                'Hu2 Rotado': momentos_rotados[1],
                'Hu3 Rotado': momentos_rotados[2]
            }
            resultados.append(fila)
    
    # Crear DataFrame
    df = pd.DataFrame(resultados)
    df.to_csv('resultados/momentos_hu_rotacion.csv', index=False)
    print(df)
    
    return df

# Directorio de imágenes
carpeta_binarias = "Imagenes_binarias"

# Ejecutar procesamiento
procesar_imagenes(carpeta_binarias)
