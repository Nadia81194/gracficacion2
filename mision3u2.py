import cv2
import numpy as np
import math

sello = np.zeros((600, 600, 3), dtype=np.uint8)
sello[:] = (40, 20, 20)

cv2.circle(sello, (300, 300), 170, (0, 255, 255), 3)
cv2.circle(sello, (300, 300), 110, (0, 255, 255), 2)

cv2.rectangle(sello, (250, 260), (350, 340), (0, 0, 255), -1)

cv2.line(sello, (0, 0), (600, 600), (255, 255, 255), 2)
cv2.line(sello, (600, 0), (0, 600), (255, 255, 255), 2)

cx = 300
cy = 300
d = 140

for i in range(8):
    a = i * (360 / 8)
    r = a * (3.1416 / 180)
    x = int(cx + d * math.cos(r))
    y = int(cy + d * math.sin(r))
    cv2.circle(sello, (x, y), 8, (0, 255, 0), -1)

f = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(sello, "SECTOR-9", (210, 560), f, 1.5, (255, 255, 255), 3)

cv2.imwrite("m3_sello", sello)
cv2.imshow("sello", sello)
cv2.waitKey(0)
cv2.destroyAllWindows()