import cv2
import numpy as np

path = r'C:\Users\tigre\Downloads\frutas.png'
img = cv2.imread(path)

if img is None:
    print("Error: No se pudo cargar la imagen. Verifica la ruta.")
else:

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    cv2.imshow('frutas', img)
    cv2.imshow(' HSV', hsv)
    cv2.imshow('mascara amarilla', mask)

    
    cv2.waitKey(0)
    cv2.destroyAllWindows()