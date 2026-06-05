import cv2
import numpy as np
import time

# Cargar la imagen
img = cv2.imread('C:\\Users\\Yagoc\\OneDrive\\Desktop\\Tareas_grafi\\Traslacion_Rotacion_Escalamiento\\vehiculo.jpg')
h, w = img.shape[:2]  # 600 alto, 800 ancho
tx, ty = 300, 200     # desplazamiento: 300 derecha, 200 abajo

# MÉTODO 1: MODO RAW (Slicing de NumPy)

inicio = time.time()

lienzo_raw = np.zeros((h, w, 3), dtype=np.uint8)
lienzo_raw[ty:h, tx:w] = img[0:h-ty, 0:w-tx]

fin = time.time()
print(f"Modo Raw:    {fin - inicio:.6f} segundos")

# MÉTODO 2: MODO OPENCV (cv2.warpAffine)

inicio = time.time()

M = np.float32([[1, 0, tx],
                [0, 1, ty]])
resultado_cv = cv2.warpAffine(img, M, (w, h))

fin = time.time()
print(f"Modo OpenCV: {fin - inicio:.6f} segundos")

# Mostrar
cv2.imshow('Original',     img)
cv2.imshow('Raw',          lienzo_raw)
cv2.imshow('OpenCV',       resultado_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()