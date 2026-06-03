import cv2
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

marcador_aruco = cv2.aruco.generateImageMarker(diccionario, id=24, sidePixels=400)

cv2.imwrite(r'C:\Users\tigre\Downloads\marcador_aruco.png', marcador_aruco)

cv2.imshow("Muestra este marcador en tu celular", marcador_aruco)
cv2.waitKey(0)
cv2.destroyAllWindows()