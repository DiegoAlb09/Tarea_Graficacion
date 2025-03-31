import cv2
import numpy as np 
import os
import matplotlib.pyplot as plt 

def obtener_contorno_vecindad_8(imagen_binaria):
    """
    Obtiene el contorno de objetos binarios usando vecindad-8
    """
    # Asegurarse que la imagen sea binaria
    if len(imagen_binaria.shape) > 2:
        imagen_binaria = cv2.cvtColor(imagen_binaria, cv2.COLOR_BGR2GRAY)
    
    # Binarizar si no está completamente binaria
    _, imagen_binaria = cv2.threshold(imagen_binaria, 127, 255, cv2.THRESH_BINARY)
    
    # Copiar imagen para no modificar la original
    contorno = imagen_binaria.copy()
    alto, ancho = imagen_binaria.shape
    
    # Kernel de vecindad-8
    vecinos_8 = [
        (-1,-1), (-1,0), (-1,1),
        (0,-1),           (0,1),
        (1,-1), (1,0), (1,1)
    ]
    
    # Matriz para marcar contornos
    contornos = np.zeros_like(contorno)
    
    # Recorrer cada pixel
    for y in range(1, alto-1):
        for x in range(1, ancho-1):
            # Si el pixel actual es blanco
            if imagen_binaria[y,x] == 255:
                # Verificar vecinos
                es_contorno = False
                for dy, dx in vecinos_8:
                    # Si algún vecino es negro, es contorno
                    if imagen_binaria[y+dy, x+dx] == 0:
                        es_contorno = True
                        break
                
                # Marcar como contorno
                if es_contorno:
                    contornos[y,x] = 255
    
    return contornos

def graficar_contorno(imagen, nombre, contorno):
    """
    Grafica la imagen original y su contorno
    """
    plt.figure(figsize=(15,5))
    
    # Imagen original
    plt.subplot(131)
    plt.imshow(imagen, cmap='gray')
    plt.title(f'Imagen Original: {nombre}')
    plt.axis('off')
    
    # Imagen binaria
    #plt.subplot(132)
    #plt.imshow(imagen, cmap='gray')
    #plt.title(f'Imagen Binaria: {nombre}')
    #plt.axis('off')
    
    # Contorno
    plt.subplot(133)
    plt.imshow(contorno, cmap='gray')
    plt.title(f'Contorno Vecindad-8: {nombre}')
    plt.grid(True, color='red', linestyle='--', linewidth=0.5)
    
    # Información de contorno
    contorno_pixeles = np.sum(contorno == 255)
    total_pixeles = imagen.shape[0] * imagen.shape[1]
    
    plt.text(1.05, 0.5, 
             f"Pixeles de Contorno: {contorno_pixeles}\n" +
             f"% Contorno: {contorno_pixeles/total_pixeles*100:.2f}%", 
             transform=plt.gca().transAxes, 
             verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(f'contornos/{nombre}_contorno.png')
    plt.close()

def procesar_imagenes(directorio):
    # Crear carpeta para contornos si no existe
    os.makedirs('contornos', exist_ok=True)
    
    # Filtrar solo archivos PNG
    archivos = [f for f in os.listdir(directorio) if f.endswith('.png')]
    print(f"Archivos en '{directorio}': {archivos}")
    
    for archivo in archivos:
        ruta = os.path.join(directorio, archivo)
        
        # Cargar imagen en escala de grises
        imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
        
        # Obtener contorno
        contorno = obtener_contorno_vecindad_8(imagen)
        
        # Graficar y guardar
        graficar_contorno(imagen, archivo, contorno)

# Directorio de imagenes binarias
carpeta_binarias = "Imagenes_binarias"

# Procesar imagenes 
procesar_imagenes(carpeta_binarias)
