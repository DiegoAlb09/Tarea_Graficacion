import cv2
import numpy as np 
import os

carpeta = "Imagenes_binarias/" #Ruta de la carpeta con lista_imagenes
archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith(".png")]

pixeles_objetos = []

#Crear carpeta de las imagenes escaladas 
if not os.path.exists("Imagenes_escaladas"):
    os.makedirs("Imagenes_escaladas")
    
#1. Contar los pixeles 1 en cada imagenes
for ruta in archivos:
    imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

    #Verificar si se cargo la imagen
    if imagen is None:
        print(f"Error al cargar la imagen: {ruta}")
        continue

    _, imagen_binaria = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)
    num_pixeles_objeto = np.count_nonzero(imagen_binaria == 255)

    pixeles_objetos.append((ruta, num_pixeles_objeto))

#2. Calcular el tamaño objetivo (media de pixeles 1)
tamanio_objetivo = int(np.mean([num for _, num in pixeles_objetos if num > 0]))
print(f"Tamaño objetivo (media de píxeles de objeto): {tamanio_objetivo}")

#3. Aplicar escalado a cada imagen
for ruta, pixeles_actual in pixeles_objetos:
    if pixeles_actual == 0:
        print(f"{ruta} no tiene pixeles de objeto, se omite.")
        continue

    #Calcular el factor de escala 
    factor_a = np.sqrt(tamanio_objetivo / pixeles_actual)

    #Cargar la imagen original
    imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    _, imagen_binaria = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)

    #Calcular el nuevo tamaño 
    nuevo_tamanio = (int(imagen.shape[1] * factor_a), int(imagen.shape[0] * factor_a))

    #Redimensionar la imagen 
    imagen_escalada = cv2.resize(imagen_binaria, nuevo_tamanio, interpolation = cv2.INTER_NEAREST)

    # Contar los píxeles de objeto en la imagen escalada
    num_pixeles_objeto_escalada = np.count_nonzero(imagen_escalada == 255)

    #Guardar la imagen transformada
    nueva_ruta = f"Imagenes_escaladas/{os.path.basename(ruta)}"
    cv2.imwrite(nueva_ruta, imagen_escalada)

    print(f"{os.path.basename(ruta)}:")
    print(f"  - Píxeles originales: {pixeles_actual}")
    print(f"  - Píxeles después del escalado: {num_pixeles_objeto_escalada}")
    print(f"  - Factor de escala: {factor_a:.3f}")
    print(f"  - Nuevo tamaño: {nuevo_tamanio}")
    print(f"  - Diferencia con el objetivo: {num_pixeles_objeto_escalada - tamanio_objetivo} píxeles")
    print("-" * 50)
