import cv2 as cv
import numpy as np

# Leer la imagen
img = cv.imread('C:\\Users\\Yagoc\\OneDrive\\Desktop\\Tareas_grafi\\Segmentacion_Frutas\\frutas.png')

# Convertir la imagen al espacio de color HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Rangos HSV por color
lower_green  = np.array([35, 100, 100]);  upper_green  = np.array([85,  255, 255])
lower_red1   = np.array([170, 100, 100]); upper_red1   = np.array([180, 255, 255])
lower_red2   = np.array([0,  100, 100]);  upper_red2   = np.array([10,  255, 255])
lower_yellow = np.array([25, 100, 100]);  upper_yellow = np.array([35,  255, 255])

# Máscaras binarias
mask_green  = cv.inRange(hsv, lower_green,  upper_green)
mask_red    = cv.inRange(hsv, lower_red1,   upper_red1) | cv.inRange(hsv, lower_red2, upper_red2)
mask_yellow = cv.inRange(hsv, lower_yellow, upper_yellow)

# ── Actividad 2: Limpieza morfológica ──────────────────────────────────────
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))

mask_green_clean  = cv.morphologyEx(mask_green,  cv.MORPH_OPEN, kernel, iterations=2)
mask_red_clean    = cv.morphologyEx(mask_red,    cv.MORPH_OPEN, kernel, iterations=2)
mask_yellow_clean = cv.morphologyEx(mask_yellow, cv.MORPH_OPEN, kernel, iterations=2)

# ── Actividad 3: Conteo de regiones conectadas ─────────────────────────────
def contar_frutas(mask, nombre, area_min=2000):
    num_labels, _, stats, _ = cv.connectedComponentsWithStats(mask, connectivity=8)
    areas = [stats[i, cv.CC_STAT_AREA] for i in range(1, num_labels)
             if stats[i, cv.CC_STAT_AREA] >= area_min]
    print(f"{nombre}: {len(areas)} frutas detectadas — áreas: {areas}")

contar_frutas(mask_green_clean,"Verde")
contar_frutas(mask_red_clean,"Rojo")
contar_frutas(mask_yellow_clean,"Amarillo")


# ── Mostrar resultados ─────────────────────────────────────────────────────
cv.imshow("Imagen Original",img)
cv.imshow("HSV",hsv)
cv.imshow("Máscara Verde - cruda",mask_green)
cv.imshow("Máscara Verde - limpia",mask_green_clean)
cv.imshow("Máscara Rojo  - cruda",mask_red)
cv.imshow("Máscara Rojo  - limpia",mask_red_clean)
cv.imshow("Máscara Amarillo - cruda",mask_yellow)
cv.imshow("Máscara Amarillo - limpia",mask_yellow_clean)

cv.waitKey(0)
cv.destroyAllWindows()
