import cv2
import numpy as np
import math

# Cargar la imagen
img = cv2.imread('C:\\Users\\Yagoc\\OneDrive\\Desktop\\Tareas_grafi\\Traslacion_Rotacion_Escalamiento\\qr_rotado.jpg')
h, w = img.shape[:2]  # 500x500
cx, cy = 250, 250     # centro de la imagen
angulo = -45          # sentido horario
rad = math.radians(angulo)

# ==========================================
# MÉTODO 1: MODO RAW (Trigonometría inversa)
# ==========================================
lienzo_raw = np.zeros((h, w, 3), dtype=np.uint8)

for y_dst in range(h):
    for x_dst in range(w):
        # Coordenadas relativas al centro
        x_c = x_dst - cx
        y_c = y_dst - cy

        # Rotación inversa (de destino a origen)
        x_src = int( x_c * math.cos(rad) - y_c * math.sin(rad) + cx)
        y_src = int( x_c * math.sin(rad) + y_c * math.cos(rad) + cy)

        # Solo copiar si el píxel origen existe dentro de la imagen
        if 0 <= x_src < w and 0 <= y_src < h:
            lienzo_raw[y_dst, x_dst] = img[y_src, x_src]

# ==========================================
# MÉTODO 2: MODO OPENCV
# ==========================================
M = cv2.getRotationMatrix2D((cx, cy), -45, 1.0)
resultado_cv = cv2.warpAffine(img, M, (w, h))

# Mostrar
cv2.imshow('Original',  img)
cv2.imshow('Raw',       lienzo_raw)
cv2.imshow('OpenCV',    resultado_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()