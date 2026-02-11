import numpy as np
import cv2 as cv 

img = np.ones((400,400), np.uint8)*255
img[1,1]=0
for i in range(100):
    img[i,i]=0
cv.imshow('imagen', img)
cv.waitKey()
cv.destroyAllWindows()