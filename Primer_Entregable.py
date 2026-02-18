import cv2 as cv
import numpy as np

# Leer la imagen
img = cv.imread('C:\\Users\\Yagoc\\OneDrive\\Desktop\\Tareas_grafi\\Imagenes\\Quinto_ejercicio\\frutas.png')

# Convertir la imagen al espacio de color HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Definir el rango inferior y superior para detectar verde
lower_green = np.array([35, 100, 100])  # Hue, Saturación, Brillo mínimos
upper_green = np.array([85, 255, 255])  # Hue, Saturación, Brillo máximos
lower_red1 = np.array([170, 100, 100])  # Hue, Saturación, Brillo mínimos
upper_red1 = np.array([180, 255, 255])  # Hue, Saturación, Brillo máximos
lower_red2 = np.array([0, 100, 100])  # Hue, Saturación, Brillo mínimos
upper_red2 = np.array([10, 255, 255])  # Hue, Saturación, Brillo máximos
lower_yellow = np.array([25, 100, 100])  # Hue, Saturación, Brillo mínimos
upper_yellow = np.array([35, 255, 255])  # Hue, Saturación, Brillo máximos

# Crear una máscara que solo incluya los píxeles dentro del rango
mask_green = cv.inRange(hsv, lower_green, upper_green)
mask_red1 = cv.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv.inRange(hsv, lower_red2, upper_red2)
mask_yellow = cv.inRange(hsv, lower_yellow, upper_yellow)

# Aplicar la máscara a la imagen original
result_green = cv.bitwise_and(img, img, mask=mask_green)
result_red = cv.bitwise_and(img, img, mask=mask_red1) + cv.bitwise_and(img, img, mask=mask_red2)
result_yellow = cv.bitwise_and(img, img, mask=mask_yellow)

# Mostrar la imagen original y la imagen con el color detectado
cv.imshow("Imagen Original", img)
cv.imshow("Color Detectado - Verde", result_green)
cv.imshow("Color Detectado - Rojo", result_red)
cv.imshow("Color Detectado - Amarillo", result_yellow)
cv.waitKey(0)
cv.destroyAllWindows()