import cv2
import numpy as np

img = cv2.imread("Imagenes/m4_ruido.png")

kernel = np.array([[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]], dtype=np.float32) / 9.0

img_suavizada = cv2.filter2D(img, -1, kernel)

hsv = cv2.cvtColor(img_suavizada, cv2.COLOR_BGR2HSV)

lower_cyan = np.array([80, 50, 50])
upper_cyan = np.array([100, 255, 255])

mask_cyan = cv2.inRange(hsv, lower_cyan, upper_cyan)

cv2.imshow("Original", img)
cv2.imshow("Mascara Cyan", mask_cyan)
cv2.imshow("Suavizada (Filtro 3x3)", img_suavizada)

cv2.waitKey(0)
cv2.destroyAllWindows()