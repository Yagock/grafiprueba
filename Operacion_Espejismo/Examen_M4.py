import cv2 as cv
import numpy as np

img = cv.imread('Imagenes/m4_ruido.png')

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
lower_cyan = np.array([80, 100, 100])
upper_cyan = np.array([100, 255, 255])
mask = cv.inRange(hsv, lower_cyan, upper_cyan)

cv.imshow("Imagen Original", img)
cv.imshow("Mascara Cyan", mask)
cv.waitKey(0)
cv.destroyAllWindows()