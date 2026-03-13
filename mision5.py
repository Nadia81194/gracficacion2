# 1. Crea lienzo 500x500
# 2. Bucle para t de 0 a 6.28 con incrementos de 0.01
# 3. Calcula x e y, redondéalos a int
# 4. Usa cv2.circle(lienzo, (x, y), 1, (255, 255, 255), -1) para pintar el punto
import math 
import cv2
import numpy as np

resultado_final = np.zeros((500, 500, 3), np.uint8)
t = 0.0
# para que no queden huecos en el dibujo
salto = 0.01 

# t va hasta 2*pi (6.28 mas o menos)
while t < 6.29:
    x_calculada = 250 + 150 * math.sin(3 * t)
    y_calculada = 250 + 150 * math.sin(2 * t)
    
    # tuve que poner int() porque cv2.circle no acepta decimales y me tiraba error el programa
    punto_x = int(x_calculada)
    punto_y = int(y_calculada)
    
    cv2.circle(resultado_final, (punto_x, punto_y), 1, (255, 255, 255), -1)
    t = t + salto

cv2.imshow('La Antena Parabólica', resultado_final)
cv2.waitKey(0)
cv2.destroyAllWindows()