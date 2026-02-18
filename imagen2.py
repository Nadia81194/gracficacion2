import cv2
import numpy as np

img1 = cv2.imread(r'C:\Users\tigre\Downloads\kir.jpeg')

# Obtener dimensiones (filas, columnas, canales)
x, y, z = img1.shape
print(f"Dimensiones: {x}, {y}, {z}")

img2 = np.zeros((x, y), np.uint8)

# Dividir la imagen original en sus canales azul (b), verde (g) y rojo (r)
b, g, r = cv2.split(img1)

# Crear versiones resaltando un solo color (poniendo los otros canales en negro)
mr = cv2.merge([img2, img2, r]) # Solo Rojo
mg = cv2.merge([img2, g, img2]) # Solo Verde
mb = cv2.merge([b, img2, img2]) # Solo Azul

# Mezclar canales en diferentes órdenes
nueva = cv2.merge([r, g, b])  # RGB (OpenCV usa BGR por defecto, así que esto invierte colores)
nueva2 = cv2.merge([g, b, r]) 
nueva3 = cv2.merge([b, r, g])

# Mostrar las ventanas con los resultados
cv2.imshow('n1', nueva)
cv2.imshow('n2', nueva2)
cv2.imshow('n3', nueva3)
cv2.imshow('b', mb)
cv2.imshow('g', mg)
cv2.imshow('r', mr)
cv2.imshow('img', img1)

cv2.waitKey(0)
cv2.destroyAllWindows()