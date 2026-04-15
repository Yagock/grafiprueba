import cv2
import numpy as np

img = cv2.imread("Imagenes/m1_oscura 1.png", cv2.IMREAD_GRAYSCALE)

# TODO MODO RAW:
# - Crear una matriz int32 para evitar overflow
# - Recorrer con ciclos anidados (y,x)
# - Multiplicar cada píxel por 50
# - Aplicar np.clip a 0..255 y guardar como uint8 -> m1_recuperado_x50.png

img_int = img.astype(np.int32)
alto, ancho = img.shape
recuperado_x50 = np.zeros((alto, ancho), dtype=np.int32)

for y in range(alto):
    for x in range(ancho):
        valor = img_int[y, x] * 50
        valor = np.clip(valor, 0, 255)
        recuperado_x50[y, x] = valor

recuperado_x50 = recuperado_x50.astype(np.uint8)

# TODO SEGUNDA FASE (RAW):
# - Sumar +20 a cada píxel recuperado
# - Aplicar np.clip 0..255 y guardar -> m1_recuperado_x50_mas20.png

recuperado_x50_mas20 = np.zeros((alto, ancho), dtype=np.int32)

for y in range(alto):
    for x in range(ancho):
        valor = recuperado_x50[y, x] + 20
        valor = np.clip(valor, 0, 255)
        recuperado_x50_mas20[y, x] = valor

recuperado_x50_mas20 = recuperado_x50_mas20.astype(np.uint8)

# TODO MODO VECTORIZADO (opcional):
# - Hacer lo mismo sin for (con operaciones NumPy o cv2.multiply/cv2.add)

vec_x50 = np.clip(img.astype(np.int32) * 50, 0, 255).astype(np.uint8)
vec_x50_mas20 = np.clip(vec_x50.astype(np.int32) + 20, 0, 255).astype(np.uint8)

cv2.imshow("Original", img)
cv2.imshow("RAW x50", recuperado_x50)
cv2.imshow("RAW x50 + 20", recuperado_x50_mas20)
cv2.imshow("Vectorizado x50", vec_x50)
cv2.imshow("Vectorizado x50 + 20", vec_x50_mas20)

cv2.waitKey(0)
cv2.destroyAllWindows()