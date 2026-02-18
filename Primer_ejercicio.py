import cv2 as cv
import numpy as np

i = j = 0

# Crear imagen blanca de 400x400
img = np.ones([400, 400], np.uint8) * 255

img[1, 1] = 0
img[400, 400] = 1

for i in range(400):
    for j in range(400):
        img[i, j] = 255 - i

cv.imshow("imagen", img)
cv.waitKey(0)
cv.destroyAllWindows()