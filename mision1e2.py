import cv2
import numpy as np

ruta_imagen = r'C:\Users\tigre\Downloads\m1_oscura 1.png'
foto = cv2.imread(ruta_imagen, 0)

if foto is not None:
    alto, ancho = foto.shape
    
    capa1 = np.zeros((alto, ancho), dtype=np.int32)
    for i in range(0, alto):
        for j in range(0, ancho):
            pixel = foto[i, j]
            nuevo_p = pixel * 50
            if nuevo_p > 255:
                nuevo_p = 255
            capa1[i, j] = nuevo_p

    capa2 = np.zeros((alto, ancho), dtype=np.int32)
    for i in range(alto):
        for j in range(ancho):
            val = foto[i, j]
            res = (val * 50) + 20
            if res > 255:
                res = 255
            if res < 0:
                res = 0
            capa2[i, j] = res

    final1 = capa1.astype(np.uint8)
    final2 = capa2.astype(np.uint8)

    cv2.imshow('Resultado 1', final1)
    cv2.imshow('Resultado 2', final2)
    
    print("Mostrando imagenes...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("no se encontro el archivo")