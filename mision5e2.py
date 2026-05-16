import cv2
import numpy as np
img = np.random.randint(0, 255, (300, 700, 3), dtype=np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, "CODIGO_SECRETO_5", (50, 150), font, 2, (30, 240, 120), 5)

b, g, r = cv2.split(img)
diff_gb = cv2.absdiff(g, b)
resta_rg = cv2.subtract(r, g)
_, mensaje_final = cv2.threshold(diff_gb, 50, 255, cv2.THRESH_BINARY)

cv2.imshow("B (Azul)", b)
cv2.imshow("G (Verde)", g)
cv2.imshow("R (Rojo)", r)
cv2.imshow("Prueba(G-B)", diff_gb)
cv2.imshow("Prueba R-G", resta_rg)
cv2.imshow("Mensaje ", mensaje_final)

cv2.waitKey(0)
cv2.destroyAllWindows()