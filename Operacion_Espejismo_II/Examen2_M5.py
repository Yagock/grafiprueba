import cv2
import numpy as np

img = np.random.randint(0, 256, (300, 700, 3), dtype=np.uint8)

texto = "CLAVE: GRAFICA-2026"
cv2.putText(img, texto, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 0), 5)

b, g, r = cv2.split(img)

res_diff = cv2.absdiff(g, b)

_, mensaje_final = cv2.threshold(res_diff, 200, 255, cv2.THRESH_BINARY)

cv2.imshow("Original (m5_tricolor)", img)
cv2.imshow("Canal G (Pista)", g)
cv2.imshow("Diferencia abs(G-B)", res_diff)
cv2.imshow("Mensaje Recuperado", mensaje_final)

cv2.waitKey(0)
cv2.destroyAllWindows()