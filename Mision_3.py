import cv2
import numpy as np

img_microfilm = cv2.imread('Imagenes/microfilm.jpg')

if img_microfilm is None:
    print("Error: No se pudo cargar la imagen.")
    exit()
recorte = img_microfilm[900:1100, 900:1100]
escala = 5

alto, ancho, canales = recorte.shape

nuevo_alto = alto * escala
nuevo_ancho = ancho * escala
raw_escalado = np.zeros((nuevo_alto, nuevo_ancho, canales), dtype=np.uint8)
for y in range(alto):
    for x in range(ancho):

        pixel = recorte[y, x]

        for dy in range(escala):
            for dx in range(escala):

                raw_escalado[y*escala + dy, x*escala + dx] = pixel

opencv_escalado = cv2.resize(
    recorte,
    None,
    fx=5,
    fy=5,
    interpolation=cv2.INTER_CUBIC
)

cv2.imshow("Imagen Original", img_microfilm)
cv2.imshow("Recorte Central", recorte)
cv2.imshow("Escalado RAW (Vecino cercano)", raw_escalado)
cv2.imshow("Escalado OpenCV INTER_CUBIC", opencv_escalado)

cv2.waitKey(0)
cv2.destroyAllWindows()