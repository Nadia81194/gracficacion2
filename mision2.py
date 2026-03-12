# mitad1 = cv2.imread('m2_mitad1.png')
# mitad2 = cv2.imread('m2_mitad2.png')

# 1. Crea lienzo de 400x400
# 2. Traslada la mitad 1 y pégala
# 3. Rota la mitad 2, trasládala y pégala

import cv2
import numpy as np

parte1 = cv2.imread(r'C:\Users\tigre\Downloads\m2_mitad1.png')
parte2 = cv2.imread(r'C:\Users\tigre\Downloads\m2_mitad2.png')

lienzo_final = np.zeros((400, 400, 3), np.uint8)

# Trasladar la mitad 1

M_traslacion = np.float32([[1, 0, 0], [0, 1, 0]])
# aplico el warpAffine 
mitad1_lista = cv2.warpAffine(parte1, M_traslacion, (400, 200))
lienzo_final[0:200, 0:400] = mitad1_lista

#  Rota la mitad 2
alto2 = parte2.shape[0]
ancho2 = parte2.shape[1]
# el centro es la mitad de la imagen
centro_profe = (ancho2 // 2, alto2 // 2)

# rotacion 180
M_rotar = cv2.getRotationMatrix2D(centro_profe, 180, 1)
mitad2_derecha = cv2.warpAffine(parte2, M_rotar, (ancho2, alto2))
lienzo_final[200:400, 0:400] = mitad2_derecha

# resultado final 
cv2.imshow('QR completo', lienzo_final)

cv2.waitKey(0)
cv2.destroyAllWindows()