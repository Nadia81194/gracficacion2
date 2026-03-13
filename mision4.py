# img = cv2.imread('m4_ruido.png')

# 1. Convertir a HSV
# 2. Crear máscara con cv2.inRange
# 3. Mostrar la máscara para leer la clave

import cv2
import numpy as np

foto_ruido = cv2.imread(r'C:\Users\tigre\Downloads\m4_ruido.png')

imagen_hsv = cv2.cvtColor(foto_ruido, cv2.COLOR_BGR2HSV)

# Cyan = 90
bajo = np.array([80, 100, 100])
alto = np.array([100, 255, 255])

mascara = cv2.inRange(imagen_hsv, bajo, alto)
 #limpiando los puntos blancos 
kernel = np.ones((3,3), np.uint8)
clean = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
final = cv2.dilate(clean, kernel, iterations=1)

cv2.imshow('Original', foto_ruido)
cv2.imshow('Macara', mascara)
cv2.imshow('La Frecuencia Térmica (Modelo HSV)', final)


cv2.waitKey(0)
cv2.destroyAllWindows()