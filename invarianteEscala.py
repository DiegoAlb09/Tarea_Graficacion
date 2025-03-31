import cv2
import numpy as np
import os
import pandas as pd

def calcular_momentos_invariantes(imagen):
    # Calcular momentos centrales de la imagen
    momentos = cv2.moments(imagen)
    
    # Extraer los valores necesarios
    mu_00 = momentos['m00']
    
    if mu_00 == 0:
        return None  # Evitar divisiones por cero
    
    # Calcular momentos centrales
    mu_10 = momentos['m10']
    mu_01 = momentos['m01']
    mu_11 = momentos['m11']
    mu_20 = momentos['m20']
    mu_02 = momentos['m02']
    
    # Calcular momentos centrales normalizados
    mu_10_normalizado = mu_10 / mu_00
    mu_01_normalizado = mu_01 / mu_00
    
    # Calcular momentos centrales de segundo orden
    mu_20_normalizado = mu_20 / (mu_00 ** 2)
    mu_02_normalizado = mu_02 / (mu_00 ** 2)
    mu_11_normalizado = mu_11 / (mu_00 ** 2)
    
    # Calcular invariantes de escala ηpq
    return (mu_10_normalizado, mu_01_normalizado, mu_11_normalizado, 
            mu_20_normalizado, mu_02_normalizado)

carpeta_original = "Imagenes_binarias/"
carpeta_escalada = "Imagenes_escaladas/"

#print("Archivos en 'imagenes_binarias/':", os.listdir(carpeta_original))
#print("Archivos en 'imagenes_escaladas/':", os.listdir(carpeta_escalada))

# Crear lista de imágenes originales y escaladas
archivos = [f for f in os.listdir(carpeta_original) if f.endswith(".png")]

# Tabla para almacenar resultados
resultados = []

for archivo in archivos:
    # Cargar imágenes original y escalada
    imagen_original = cv2.imread(os.path.join(carpeta_original, archivo), cv2.IMREAD_GRAYSCALE)
    imagen_escalada = cv2.imread(os.path.join(carpeta_escalada, archivo), cv2.IMREAD_GRAYSCALE)

    # Verificar si las imágenes se cargaron correctamente
    if imagen_original is None:
        print(f"No se pudo cargar la imagen original: {archivo}")
        continue
    if imagen_escalada is None:
        print(f"No se pudo cargar la imagen escalada: {archivo}")
        continue 

    # Binarizar las imágenes
    _, imagen_original = cv2.threshold(imagen_original, 127, 255, cv2.THRESH_BINARY)
    _, imagen_escalada = cv2.threshold(imagen_escalada, 127, 255, cv2.THRESH_BINARY)

    # Calcular invariantes de escala
    momentos_original = calcular_momentos_invariantes(imagen_original)
    momentos_escalada = calcular_momentos_invariantes(imagen_escalada)

    if momentos_original and momentos_escalada:
        resultados.append([archivo] + list(momentos_original) + list(momentos_escalada))

# Crear un DataFrame de Pandas
columnas = ["Imagen", 
            "η_10 (Antes)", "η_01 (Antes)", "η_11 (Antes)", "η_20 (Antes)", "η_02 (Antes)",
            "η_10 (Después)", "η_01 (Después)", "η_11 (Después)", "η_20 (Después)", "η_02 (Después)"]

df = pd.DataFrame(resultados, columns=columnas)

# Guardar en CSV y mostrar la tabla
df.to_csv("momentos_invariantes.csv", index=False)
print(df)
