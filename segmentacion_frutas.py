import cv2
import numpy as np

path = r'C:\Users\tigre\Downloads\frutas.png'
img = cv2.imread(path)

if img is None:
    print("no carga la imagen otra vez")
else:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # actividad 1 detectar los colores amarillos
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # actividad 2 quitar el "ruido"
    kernel = np.ones((5,5), np.uint8)
    mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask_final = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel)

    # actividad 3 conteo

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_final)
    
    # aqyi se aplica un filtro para que solo cuante las areas grandes de color amerillo para no contar pequeños segmentos
    conteo = 0
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area > 500: 
            conteo += 1

    print(f"total del conteo: {conteo}")

    # Mostrar resultados
    cv2.imshow('mascara original', mask)
    cv2.imshow('mascara sin ruido', mask_final)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()