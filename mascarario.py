import cv2
import numpy as np

path = r'C:\Users\tigre\Downloads\frutas.png'
img = cv2.imread(path)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


# Amarillo
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([32, 255, 255])

# Verde
lower_green = np.array([35, 50, 50])
upper_green = np.array([85, 255, 255])

# Rojo

lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])



mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
mask_green = cv2.inRange(hsv, lower_green, upper_green)

mask_red_low = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red_high = cv2.inRange(hsv, lower_red2, upper_red2)
mask_red = cv2.bitwise_or(mask_red_low, mask_red_high)



cv2.imshow('Frutas colores', img)
cv2.imshow('mascara amarilla', mask_yellow)
cv2.imshow('mascara verde', mask_green)
cv2.imshow('mascara roja ', mask_red)

cv2.waitKey(0)
cv2.destroyAllWindows()