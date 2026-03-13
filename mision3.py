# 1. Crea el lienzo con color base
# 2. Dibuja círculo, rectángulo y líneas en ese orden exacto.

import cv2
import numpy as np

# lienzo de 500x500
# azul oscuro BGR(50, 20, 20)


# primero hago el fondo negro con np.zeros
sello = np.zeros((500, 500, 3), np.uint8)

# color azul oscuro a todo el fondo
sello[:] = (60, 30, 20) 

# Creando el circulo amarillo 
centro = (250, 250)
radio = 100
color_amarillo = (0, 255, 255)
cv2.circle(sello, centro, radio, color_amarillo, 3)

#rectangulo rojo solido (200,200) a (300,300)
# Para que sea solido (relleno) hay que poner -1 en el grosor
cv2.rectangle(sello, (200, 200), (300, 300), (0, 0, 255),-1)

# lineas blancas cruzadas
#  esquina a esquina seria de (0,0) a (500,500)
cv2.line(sello, (0, 0), (500, 500), (255, 255, 255),2)
cv2.line(sello, (500, 0), (0, 500), (255, 255, 255), 2)

# 5. Guardar el dibujo
cv2.imwrite('m3_sello_forjado.png', sello)


cv2.imshow('El Sello Biométrico', sello)


cv2.waitKey(0)
cv2.destroyAllWindows()