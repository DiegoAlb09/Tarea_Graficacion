# Repositorio de Procesamiento de Imágenes y Visión por Computadora

Este repositorio contiene una colección de scripts en Python para tareas básicas de procesamiento de imágenes y visión por computadora, enfocándose en análisis de imágenes binarias, extracción de características y operaciones morfológicas.

## Descripción General

El repositorio incluye scripts para:
- Visualización y análisis de imágenes binarias
- Detección de contornos
- Cálculo del centro de masa
- Invariantes de momentos (para rotación y escala)
- Escalado de imágenes
- Operaciones morfológicas
- Rotación de imágenes

## Requisitos

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Matplotlib
- Pandas

Puedes instalar todas las dependencias con:
```
pip install opencv-python numpy matplotlib pandas
```

## Estructura

### Análisis de Imágenes Binarias

- `binarioCuadricula.py`: Genera una visualización en cuadrícula de imágenes binarias con estadísticas sobre píxeles activos (píxeles blancos) y porcentaje de ocupación.

### Detección de Contornos

- `contornoImagenes.py`: Implementa detección de contornos basada en vecindad-8 para imágenes binarias y visualiza los resultados.

### Centro de Masa y Momentos

- `centroMasa.py`: Calcula el centro de masa y los momentos centrales para imágenes binarias con diferentes traslaciones.
- `invarianteEscala.py`: Calcula momentos invariantes a escala para imágenes antes y después del escalado.
- `rotacionImagen.py`: Demuestra la invariancia a la rotación calculando los momentos de Hu para imágenes en diferentes ángulos de rotación.

### Transformaciones de Imágenes

- `escalarImagenes.py`: Escala imágenes para tener un número consistente de píxeles de objeto (píxeles blancos).
- `operadoresMorfologicos.py`: Aplica operaciones morfológicas (apertura, cierre, dilatación y esqueletización) a imágenes binarias.

### Scripts de Utilidad

- `nPixeles.py`: Cuenta el número de píxeles blancos (píxeles de objeto) en imágenes binarias.

## Uso

1. Coloca tus imágenes binarias en el directorio `Imagenes_binarias`.
2. Ejecuta el script deseado, por ejemplo:
   ```
   python Graficacion/binarioCuadricula.py
   ```
3. Los resultados se guardarán en los respectivos directorios de salida:
   - `mapas_celdas/`: Visualizaciones en cuadrícula
   - `contornos/`: Imágenes de contornos
   - `Imagenes_escaladas/`: Imágenes escaladas
   - `rotaciones/`: Imágenes rotadas
   - `resultados/`: Archivos CSV con datos de momentos
   - `resultados_momentos/`: Archivos CSV con datos de momentos centrales
   - `Imagenes_apertura/`, `Imagenes_cierre/`, `Imagenes_dilatacion/`, `Imagenes_esqueleto/`: Resultados de operaciones morfológicas

## Ejemplos

### Visualización de Imágenes Binarias
El script `binarioCuadricula.py` genera una visualización de imágenes binarias con líneas de cuadrícula y calcula estadísticas como:
- Número total de celdas
- Número de píxeles activos
- Porcentaje de ocupación

### Detección de Contornos
El script `contornoImagenes.py` detecta los contornos de objetos binarios utilizando análisis de vecindad-8 y muestra:
- Imagen original
- Contorno detectado
- Estadísticas del contorno (número de píxeles, porcentaje)

### Características Invariantes a Escala
Los scripts `escalarImagenes.py` e `invarianteEscala.py` demuestran la invariancia a escala mediante:
1. Escalado de imágenes a un tamaño consistente (número medio de píxeles de objeto)
2. Cálculo de momentos centrales normalizados antes y después del escalado
3. Comparación de las propiedades invariantes de estos momentos

### Invariancia a la Rotación
El script `rotacionImagen.py` demuestra la invariancia a la rotación mediante:
1. Rotación de imágenes en diferentes ángulos (0°, 45°, 135°)
2. Cálculo de momentos de Hu para cada rotación
3. Comparación de las propiedades invariantes entre rotaciones

## Notas

- Todos los scripts esperan imágenes binarias con objetos blancos (255) sobre un fondo negro (0).
- Los scripts crean automáticamente los directorios de salida necesarios si no existen.
