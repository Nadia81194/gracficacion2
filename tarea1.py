import numpy as np
import cv2 as cv 

img = np.ones((400, 400), np.uint8) * 255

for y in range(400):
    for x in range(400):
        nx = (x - 200) / 100  
        ny = (180 - y) / 100 
        formula = (nx**2 + ny**2 - 1)**3 - (nx**2) * (ny**3)
        if formula <= 0:
            img[y, x] = 1

cv.imshow('corazon de melon', img)
cv.waitKey(0)
cv.destroyAllWindows()