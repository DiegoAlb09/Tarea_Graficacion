import cv2
import numpy as np 
import os
import matplotlib.pyplot as plt 

def generar_grafico_celdas(imagen, nombre):
    if imagen is None:
        print(f"No se puede graficar '{nombre}', imagen no cargada.")
        return
    
    # Asegurar que la imagen sea binaria
    _, imagen_binaria = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(imagen_binaria, cmap='binary', interpolation='nearest')
    plt.title(f"Mapa de Celdas Binarias: {nombre}")
    
    # Configurar cuadrícula para mostrar cada celda
    plt.grid(True, color='red', linestyle='--', linewidth=0.5)
    plt.xticks(np.arange(-0.5, imagen_binaria.shape[1], 1), [])
    plt.yticks(np.arange(-0.5, imagen_binaria.shape[0], 1), [])
    
    # Contar y marcar pixeles activos (1-pixeles)
    pixeles_activos = np.sum(imagen_binaria == 255)
    total_celdas = imagen_binaria.shape[0] * imagen_binaria.shape[1]
    porcentaje_ocupacion = (pixeles_activos / total_celdas) * 100
    
    plt.text(0.02, 0.98, 
             f"Total Celdas: {total_celdas}\n" +
             f"Pixeles Activos: {pixeles_activos}\n" +
             f"Ocupación: {porcentaje_ocupacion:.2f}%", 
             transform=plt.gca().transAxes, 
             verticalalignment='top', 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(f'mapas_celdas/{nombre}_mapa_celdas.png')
    plt.close()

def procesar_imagenes(directorio):
    # Crear carpeta para mapas de celdas si no existe
    os.makedirs('mapas_celdas', exist_ok=True)
    
    archivos = [f for f in os.listdir(directorio) if f.endswith('.png')]
    print(f"Archivos en '{directorio}': {archivos}")
    
    for archivo in archivos:
        ruta = os.path.join(directorio, archivo)
        imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
        generar_grafico_celdas(imagen, archivo)

# Directorio de imagenes binarias
carpeta_binarias = "Imagenes_binarias"

# Procesar imagenes y generar graficos 
procesar_imagenes(carpeta_binarias)
