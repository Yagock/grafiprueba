import numpy as np
import cv2 as cv
import math as m

width, height = 500, 500
img = np.zeros((height, width, 3), dtype=np.uint8)
t = 0
t_max = 6.28
incremento = 0.01

while t <= t_max:
    x = int(250 + 150 * m.sin(3 * t))
    y = int(250 + 150 * m.sin(2 * t))
    cv.circle(img, (x, y), 1, (255, 255, 255), -1)
    t += incremento

cv.imshow("Forma geometrica secreta", img)
cv.waitKey(0)
cv.destroyAllWindows()