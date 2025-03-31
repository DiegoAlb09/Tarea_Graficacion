import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

def calcular_centro_masa(imagen_binaria):
    """
    Calcula el centro de masa de una imagen binaria
    """
    # Asegurar imagen binaria
    if len(imagen_binaria.shape) > 2:
        imagen_binaria = cv2.cvtColor(imagen_binaria, cv2.COLOR_BGR2GRAY)
    _, imagen_binaria = cv2.threshold(imagen_binaria, 127, 255, cv2.THRESH_BINARY)
    
    # Calcular momentos
    momentos = cv2.moments(imagen_binaria)
    
    # Centro de masa
    if momentos['m00'] != 0:
        cx = int(momentos['m10'] / momentos['m00'])
        cy = int(momentos['m01'] / momentos['m00'])
        return cx, cy
    else:
        return None

def calcular_momentos_centrales(imagen_binaria):
    """
    Calcula momentos centrales para p,q = 0,1,2
    """
    # Asegurar imagen binaria
    if len(imagen_binaria.shape) > 2:
        imagen_binaria = cv2.cvtColor(imagen_binaria, cv2.COLOR_BGR2GRAY)
    _, imagen_binaria = cv2.threshold(imagen_binaria, 127, 255, cv2.THRESH_BINARY)
    
    # Calcular momentos
    momentos = cv2.moments(imagen_binaria)
    
    # Centro de masa
    if momentos['m00'] == 0:
        return None
    
    cx = momentos['m10'] / momentos['m00']
    cy = momentos['m01'] / momentos['m00']
    
    # Calcular momentos centrales
    momentos_centrales = {
        'µ00': momentos['m00'],
        'µ10': 0,  # Por definición de momento central
        'µ01': 0,  # Por definición de momento central
        'µ11': calcular_momento_central(imagen_binaria, 1, 1, cx, cy),
        'µ20': calcular_momento_central(imagen_binaria, 2, 0, cx, cy),
        'µ02': calcular_momento_central(imagen_binaria, 0, 2, cx, cy)
    }
    
    return momentos_centrales, (cx, cy)

def calcular_momento_central(imagen, p, q, cx, cy):
    """
    Calcula un momento central específico
    """
    momento = 0
    for y in range(imagen.shape[0]):
        for x in range(imagen.shape[1]):
            if imagen[y, x] == 255:
                momento += ((x - cx) ** p) * ((y - cy) ** q)
    return momento

def trasladar_imagen(imagen, dx, dy):
    """
    Traslada la imagen por (dx, dy)
    """
    # Crear matriz de transformación
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    
    # Aplicar transformación
    imagen_trasladada = cv2.warpAffine(imagen, M, (imagen.shape[1], imagen.shape[0]))
    
    return imagen_trasladada

def procesar_imagenes(directorio):
    # Crear carpeta para resultados si no existe
    os.makedirs('resultados_momentos', exist_ok=True)
    
    # Filtrar solo archivos PNG
    archivos = [f for f in os.listdir(directorio) if f.endswith('.png')]
    
    # Preparar lista de resultados
    resultados = []
    
    for archivo in archivos:
        ruta = os.path.join(directorio, archivo)
        
        # Cargar imagen en escala de grises
        imagen_original = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
        
        # Verificar transformaciones
        traslaciones = [
            (0, 0),    # Sin traslación
            (50, 0),   # Traslación horizontal
            (0, 50),   # Traslación vertical
            (50, 50)   # Traslación diagonal
        ]
        
        for dx, dy in traslaciones:
            # Trasladar imagen
            imagen_trasladada = trasladar_imagen(imagen_original, dx, dy)
            
            # Calcular momentos
            momentos = calcular_momentos_centrales(imagen_trasladada)
            
            if momentos:
                momentos_centrales, centro_masa = momentos
                
                # Preparar fila de resultados
                fila = {
                    'Imagen': archivo,
                    'Traslación X': dx,
                    'Traslación Y': dy,
                    'Centro Masa X': centro_masa[0],
                    'Centro Masa Y': centro_masa[1],
                    'µ00': momentos_centrales['µ00'],
                    'µ10': momentos_centrales['µ10'],
                    'µ01': momentos_centrales['µ01'],
                    'µ11': momentos_centrales['µ11'],
                    'µ20': momentos_centrales['µ20'],
                    'µ02': momentos_centrales['µ02']
                }
                
                resultados.append(fila)
    
    # Crear DataFrame
    df = pd.DataFrame(resultados)
    
    # Guardar resultados
    df.to_csv('resultados_momentos/momentos_centrales.csv', index=False)
    print(df)
    
    return df

# Directorio de imagenes binarias
carpeta_binarias = "Imagenes_binarias"

# Procesar imagenes 
procesar_imagenes(carpeta_binarias)
