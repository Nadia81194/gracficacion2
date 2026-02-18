import numpy as np
import cv2 as cv 

img = np.ones((1000, 1000), np.uint8) * 255
y_inicio, x_inicio = 25, 150
tamano = 25
cantidad1 = 7
cantidad2=5 
cantidad3=6
cantidad=3
for i in range(tamano):
    for j in range(tamano):
        img[y_inicio + i, x_inicio + j] = 0 
        img[y_inicio + i, x_inicio + j + 25] = 0 
        img[y_inicio + i, x_inicio + j + 50] = 0 
        img[y_inicio + i + 25, x_inicio + j - 25] = 0 
        img[y_inicio + i + 50, x_inicio + j - 25] = 0
        img[y_inicio + i + 75, x_inicio + j] = 0
        img[y_inicio + i + 100, x_inicio + j - 25] = 0
        img[y_inicio + i + 425, x_inicio + j-100 ] = 0
        img[y_inicio + i + 450, x_inicio + j-75 ] = 0
        img[y_inicio + i + 450, x_inicio + j-50 ] = 0
        img[y_inicio + i + 375, x_inicio + j ] = 0
        img[y_inicio + i + 550, x_inicio + j ] = 0
        img[y_inicio + i + 575, x_inicio + j+25 ] = 0
        img[y_inicio + i + 600, x_inicio + j+25 ] = 0
        img[y_inicio + i + 600, x_inicio + j+125 ] = 0
        img[y_inicio + i + 200, x_inicio + j+225 ] = 0
        img[y_inicio + i + 200, x_inicio + j+125 ] = 0

        


for n in range(cantidad1):

    y_actual = (y_inicio + 125) + (n * tamano)
    x_actual = x_inicio - 25 
    for i in range(tamano):
        for j in range(tamano):
            img[y_actual + i, x_actual + j] = 0

for n in range(cantidad2):
    y_actual = (y_inicio + 300) + (n * tamano)
    x_actual = x_inicio - (n * tamano)

    for i in range(tamano):
        for j in range(tamano):
            img[y_actual + i, x_actual + j] = 0

for n in range(cantidad3):

    y_actual = (y_inicio + 400) + (n * tamano)
    x_actual = x_inicio - 25 
    for i in range(tamano):
        for j in range(tamano):
            img[y_actual + i, x_actual + j] = 0

for n in range (cantidad):
    y_actual = y_inicio+ 625
    x_actual = (x_inicio+50) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
    
for n in range (9):
    y_actual = y_inicio+ 575
    x_actual = (x_inicio+125) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0

for n in range (cantidad):
    y_actual = y_inicio+ 625
    x_actual = (x_inicio+250) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0

for n in range (cantidad2):
    y_actual = y_inicio+ 600
    x_actual = (x_inicio+225) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
for n in range (8):
    y_actual = y_inicio+ 550
    x_actual = (x_inicio+175) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
for n in range (9):
    y_actual = y_inicio+ 525
    x_actual = (x_inicio+175) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
for n in range (9):
    y_actual = y_inicio+ 500
    x_actual = (x_inicio+175) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
for n in range (6):
    y_actual = y_inicio+ 475
    x_actual = (x_inicio+250) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
for n in range (7):
    y_actual = y_inicio+ 450
    x_actual = (x_inicio+275) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0

for n in range (8):
    y_actual = y_inicio+ 425
    x_actual = (x_inicio+275) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0

for n in range (8):
    y_actual = y_inicio+ 400
    x_actual = (x_inicio+275) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
    y_actual = y_inicio+ 400

for n in range (7):
    y_actual = y_inicio+ 375
    x_actual = (x_inicio+275) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
    y_actual = y_inicio+ 400

for n in range (7):
    y_actual = y_inicio+ 350
    x_actual = (x_inicio+250) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
    y_actual = y_inicio+ 400

for n in range (9):
    y_actual = y_inicio+ 325
    x_actual = (x_inicio+175) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
    y_actual = y_inicio+ 400
for n in range (8):
    y_actual = y_inicio+ 300
    x_actual = (x_inicio+175) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
    y_actual = y_inicio+ 400
for n in range (9):
    y_actual = y_inicio+ 275
    x_actual = (x_inicio+175) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
    y_actual = y_inicio+ 400
for n in range (9):
    y_actual = y_inicio+ 250
    x_actual = (x_inicio+175) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
    y_actual = y_inicio+ 400
for n in range (cantidad):
    y_actual = y_inicio+ 225
    x_actual = (x_inicio+150) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0
for n in range (cantidad):
    y_actual = y_inicio+ 225
    x_actual = (x_inicio+325) +(n*tamano)

    img[y_actual : y_actual + tamano, x_actual : x_actual + tamano]=0

cv.imshow('Monokuma', img)
cv.waitKey(0)
cv.destroyAllWindows()