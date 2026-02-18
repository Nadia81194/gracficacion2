import cv2 as cv

img = cv.imread(r'C:\Users\tigre\Downloads\kir.jpeg')
img = cv.resize(img, None, fx=1, fy=1)#Esto limita el tamaño
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow('hsv', hsv)
cv.imshow('imagen', img)
cv.waitKey(0)
cv.destroyAllWindows()