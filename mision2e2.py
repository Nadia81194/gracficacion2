import cv2
import numpy as np

m1 = cv2.imread(r'C:\Users\tigre\Downloads\m2_mitad1.png')
m2 = cv2.imread(r'C:\Users\tigre\Downloads\m2_mitad2.png')
lienzo = np.full((600, 600, 3), 255, dtype=np.uint8)

if m1 is not None and m2 is not None:
    h1, w1 = m1.shape[:2]
    h2, w2 = m2.shape[:2]

    # Mitad 1
    m_t = np.float32([[1, 0, 0], [0, 1, 0]])
    p1 = cv2.warpAffine(m1, m_t, (w1, h1))

    # Mitad 2
    c = (w2 // 2, h2 // 2)
    m_r = cv2.getRotationMatrix2D(c, 180, 1.0)
    p2 = cv2.warpAffine(m2, m_r, (w2, h2))

    y = 50
    x = 50
   
    lienzo[y : y + h1, x : x + w1] = p1
    lienzo[y + h1 : y + h1 + h2, x : x + w2] = p2

    cv2.imwrite(" qr reconstruido.png", lienzo)
    cv2.imshow("resultado", lienzo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("error con la ruta de las imagenes")