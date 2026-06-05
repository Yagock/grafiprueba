import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('C:\\Users\\Yagoc\\OneDrive\\Desktop\\Tareas_grafi\\Traslacion_Rotacion_Escalamiento\\microfilm.jpg')
h, w = img.shape[:2]  # 2000x2000

# Recorte de la zona central donde está el texto
cx, cy = w // 2, h // 2
recorte = img[cy-100:cy+100, cx-100:cx+100]  # 200x200 píxeles
rh, rw = recorte.shape[:2]
factor = 5

# ==========================================
# MÉTODO 1: MODO RAW (Vecino más cercano)
# ==========================================
lienzo_raw = np.zeros((rh * factor, rw * factor, 3), dtype=np.uint8)

for y in range(rh):
    for x in range(rw):
        lienzo_raw[y*factor:(y+1)*factor, x*factor:(x+1)*factor] = recorte[y, x]

# ==========================================
# MÉTODO 2: MODO OPENCV (Interpolación cúbica)
# ==========================================
resultado_cv = cv2.resize(recorte, None, fx=factor, fy=factor,
                          interpolation=cv2.INTER_CUBIC)

# Mostrar
cv2.imshow('Recorte original', recorte)
cv2.imshow('Raw',              lienzo_raw)
cv2.imshow('OpenCV',           resultado_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()