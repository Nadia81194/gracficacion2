import cv2
import numpy as np

# Cargo la imagen desde la carpeta de descargas
img_oscura = cv2.imread(r'C:\Users\tigre\Downloads\m1_oscura.png')
img_redim = cv2.resize(img_oscura, (1000, 400))

# --- MODO RAW (CON LOS FOR) ---
# Hago una copia porque si no se cambia la original
resultado1 = img_redim.copy()

# Recorro alto y ancho
for y in range(0, resultado1.shape[0]):
    for x in range(0, resultado1.shape[1]):
        for c in range(0, 3):
            # multiplico por 50 
            valor = float(resultado1[y, x, c]) * 50
            
            # esto es para que no explote el color (maximo 255)
            if valor > 255:
                resultado1[y, x, c] = 255
            else:
                resultado1[y, x, c] = int(valor)

# --- MODO OPENCV ---
resultado2 = cv2.multiply(img_redim, 50)

# Muestro los resultados
cv2.imshow('MODO RAW', resultado1)
cv2.imshow('MODO OPENCV', resultado2)

print("Mision cumplida, el codigo es ALBATROS")

cv2.waitKey(0)
cv2.destroyAllWindows()