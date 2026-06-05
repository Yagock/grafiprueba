import cv2 as cv
import numpy as np

img = cv.imread('Imagenes/m1_oscura.png', 0)
x, y = img.shape
recup = np.zeros((x, y), dtype=np.uint8)
for i in range(x):
    for j in range(y):

        val = img[i, j] * 50
        if val > 255:
            val = 255

        recup[i, j] = val

cv.imshow('Imagen oscura', img)
cv.imshow('Imagen recuperada (modo raw)', recup)

cv.waitKey(0)
cv.destroyAllWindows()