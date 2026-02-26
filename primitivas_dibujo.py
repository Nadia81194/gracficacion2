import cv2 as cv
import numpy as np

width, height = 800, 500

for i in range(0, 400, 5): 
    img = np.ones((height, width, 3), np.uint8) * 200
    
    
    # Ruedas
    cv.circle(img, (150 + i, 350), 30, (0, 0, 0), -1) # Rueda trasera
    cv.circle(img, (350 + i, 350), 30, (0, 0, 0), -1) # Rueda delantera
    
    # Carroceria 
    cv.rectangle(img, (100 + i, 250), (400 + i, 330), (50, 50, 255), -1) 
    
    # Cabina 
    cv.rectangle(img, (150 + i, 180), (320 + i, 250), (100, 100, 255), -1)
    
    # Ventana 
    cv.rectangle(img, (170 + i, 200), (230 + i, 240), (255, 255, 255), -1)
    cv.rectangle(img, (250 + i, 200), (300 + i, 240), (255, 255, 255), -1)

    # Suelo 
    cv.line(img, (0, 380), (width, 380), (50, 50, 50), 2)

    cv.imshow('bocho rojo', img)
 
    if cv.waitKey(30) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()