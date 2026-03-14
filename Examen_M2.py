import cv2 as cv
import numpy as np
mitad1 = cv.imread('Imagenes/m2_mitad1.png', 0)
mitad2 = cv.imread('Imagenes/m2_mitad2.png', 0)

x1, y1 = mitad1.shape
x2, y2 = mitad2.shape
canvas = np.zeros((400, 400), dtype=np.uint8)

dx, dy = 0, 0

M1 = np.float32([
    [1, 0, dx],
    [0, 1, dy]
])

mitad1_trans = cv.warpAffine(mitad1, M1, (400, 400))
canvas[0:x1, 0:y1] = mitad1_trans[0:x1, 0:y1]
center = (y2 // 2, x2 // 2)
M2 = cv.getRotationMatrix2D(center, 180, 1.0)
mitad2_rot = cv.warpAffine(mitad2, M2, (y2, x2))

dx2 = 0
dy2 = 200

M3 = np.float32([
    [1, 0, dx2],
    [0, 1, dy2]
])

mitad2_trans = cv.warpAffine(mitad2_rot, M3, (400, 400))
canvas[200:200+x2, 0:y2] = mitad2_trans[200:200+x2, 0:y2]


cv.imshow('Mitad 1', mitad1)
cv.imshow('Mitad 2', mitad2)
cv.imshow('Mitades reconstruidas', canvas)

cv.waitKey(0)
cv.destroyAllWindows()