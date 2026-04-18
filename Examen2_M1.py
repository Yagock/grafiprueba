import cv2
import numpy as np

img = cv2.imread("Imagenes/m1_oscura 1.png", cv2.IMREAD_GRAYSCALE)

img_int = img.astype(np.int32)
alto, ancho = img.shape
recuperado_x50 = np.zeros((alto, ancho), dtype=np.int32)

for y in range(alto):
    for x in range(ancho):
        valor = img_int[y, x] * 50
        valor = np.clip(valor, 0, 255)
        recuperado_x50[y, x] = valor

recuperado_x50 = recuperado_x50.astype(np.uint8)

recuperado_x50_mas20 = np.zeros((alto, ancho), dtype=np.int32)

for y in range(alto):
    for x in range(ancho):
        valor = recuperado_x50[y, x] + 20
        valor = np.clip(valor, 0, 255)
        recuperado_x50_mas20[y, x] = valor

recuperado_x50_mas20 = recuperado_x50_mas20.astype(np.uint8)

vec_x50 = np.clip(img.astype(np.int32) * 50, 0, 255).astype(np.uint8)
vec_x50_mas20 = np.clip(vec_x50.astype(np.int32) + 20, 0, 255).astype(np.uint8)

cv2.imshow("Original", img)
cv2.imshow("RAW x50", recuperado_x50)
cv2.imshow("RAW x50 + 20", recuperado_x50_mas20)
cv2.imshow("Vectorizado x50", vec_x50)
cv2.imshow("Vectorizado x50 + 20", vec_x50_mas20)

cv2.waitKey(0)
cv2.destroyAllWindows()