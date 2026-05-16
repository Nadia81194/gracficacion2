
import cv2
import numpy as np

img = cv2.imread(r'C:\Users\tigre\Downloads\m4_ruido.png')

kernel = np.array([[1, 1, 1], 
                   [1, 1, 1], 
                   [1, 1, 1]], dtype=np.float32) / 9

img_suave = cv2.filter2D(img, -1, kernel)

hsv = cv2.cvtColor(img_suave, cv2.COLOR_BGR2HSV)

bajo = np.array([80, 50, 50])
alto = np.array([100, 255, 255])

mascara = cv2.inRange(hsv, bajo, alto)
cv2.imshow("Imagen Suavizada", img_suave)
cv2.imshow("Mascara Cyan", mascara)
cv2.waitKey(0)
cv2.destroyAllWindows()