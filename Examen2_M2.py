import cv2
import numpy as np

mitad1 = cv2.imread("Imagenes/m2_mitad1.png")
mitad2 = cv2.imread("Imagenes/m2_mitad2.png")

lienzo = np.full((400, 400, 3), 255, dtype=np.uint8)

h1, w1 = mitad1.shape[:2]
M1 = np.float32([[1, 0, 50], [0, 1, 0]])
mitad1_enderezada = cv2.warpAffine(mitad1, M1, (w1, h1))
lienzo[0:h1, 0:w1] = mitad1_enderezada

h2, w2 = mitad2.shape[:2]
centro = (w2 // 2, h2 // 2)
M2 = cv2.getRotationMatrix2D(centro, 180, 1.0)
mitad2_enderezada = cv2.warpAffine(mitad2, M2, (w2, h2))

lienzo[h1:h1+h2, 0:w2] = mitad2_enderezada

cv2.imshow("QR Reconstruido", lienzo)

cv2.waitKey(0)
cv2.destroyAllWindows()