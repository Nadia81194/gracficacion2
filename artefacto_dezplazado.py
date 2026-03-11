import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread(r'C:\Users\tigre\Downloads\vehiculo.jpg')

alto, ancho = img.shape[:2]

# ==========================================
# MÉTODO 1: MODO RAW (Manipulación de Píxeles)
# ==========================================
# 1. Crea un lienzo negro vacío (np.zeros) de 600x800
lienzo = np.zeros((600, 800, 3), dtype=np.uint8)

# 2. Mueve los píxeles al nuevo lienzo sumando 300 en X y 200 en Y
tx, ty = 300, 200

for y in range(alto):
    for x in range(ancho):
        nuevo_x, nuevo_y = x + tx, y + ty
        
        # Verificar que el píxel esté dentro de los límites del lienzo
        if nuevo_x < 800 and nuevo_y < 600:
            lienzo[nuevo_y, nuevo_x] = img[y, x]

# ==========================================
# MÉTODO 2: MODO OPENCV (Matriz de Traslación)
# ==========================================
# 1. Crea la matriz de traslación 'M' en NumPy
# La estructura de la matriz es: [[1, 0, tx], [0, 1, ty]]
M = np.float32([[1, 0, tx], [0, 1, ty]])

# 2. Aplica cv2.warpAffine a la imagen original
# Definimos el tamaño de salida como (800, 600) para que coincida con el Método 1
metodo_opencv = cv2.warpAffine(img, M, (800, 600))

# Mostrar resultados
cv2.imshow('Metodo Raw', lienzo)
cv2.imshow('Metodo OpenCV', metodo_opencv)
cv2.waitKey(0)
cv2.destroyAllWindows()
