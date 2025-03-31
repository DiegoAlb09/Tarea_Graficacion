import cv2
import numpy as np 
import os

#Lista de rutas de las imagenes
carpeta = "Imagenes_binarias/"
archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith(".png")]
#Iterar sobre cada imagenes
for ruta in archivos:
    imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

    #Asegurar que la imagen se cargo correctamente
    if imagen is None:
        print(f"Error al cargar la imagen: {ruta}")
        continue
    
    #Asegurar que la imagen sea estrictamente binaria 
    _, imagen_binaria = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)

    #Contar los pixeles con el valor 255 (objetos en imagenes binarias)
    num_pixeles_objeto = np.count_nonzero(imagen_binaria == 255)

    #Si la imagen podría tener el objeto en negro, contar pixeles 0 tambien
    if num_pixeles_objeto == 0:
        num_pixeles_negros == np.count_nonzero(imagen_binaria == 0)
        print(f"Posible objeto negro en {ruta}, pixeles negros: {num_pixeles_negros}")

    print(f"Numero de pixeles del objeto en {ruta}: {num_pixeles_objeto}")
