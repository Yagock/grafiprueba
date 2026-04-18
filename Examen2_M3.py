import cv2
import numpy as np
import math

img = np.zeros((600, 600, 3), dtype=np.uint8)
img[:] = (40, 20, 20)

centro = (300, 300)
amarillo = (0, 255, 255)
rojo = (0, 0, 255)
blanco = (255, 255, 255)
verde = (0, 255, 0)

cv2.circle(img, centro, 170, amarillo, 3)

cv2.circle(img, centro, 110, amarillo, 2)

cv2.rectangle(img, (250, 260), (350, 340), rojo, cv2.FILLED)

cv2.line(img, (300-120, 300-120), (300+120, 300+120), blanco, 2)
cv2.line(img, (300+120, 300-120), (300-120, 300+120), blanco, 2)

for i in range(8):
    angulo = i * (2 * math.pi / 8)
    x = int(centro[0] + 140 * math.cos(angulo))
    y = int(centro[1] + 140 * math.sin(angulo))
    cv2.circle(img, (x, y), 8, verde, cv2.FILLED)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, "SECTOR-9", (230, 560), font, 1.2, blanco, 2, cv2.LINE_AA)

cv2.imshow("M3 Sello Forjado", img)

cv2.waitKey(0)
cv2.destroyAllWindows()