#  Reporte de Misión: Graficación Táctica
**Agente Especial:** Diego Santiago Zavala Urueta

---
##  Evidencias de Misión
*[Nota: Inserta aquí los bloques de código y las imágenes resultantes de las 5 Misiones]*

Misión 1:

    import cv2 as cv
    import numpy as np
    img = cv.imread('Imagenes/m1_oscura.png', 0)
    x, y = img.shape
    recup = np.zeros((x, y), dtype=np.uint8)
    for i in range(x):
        for j in range(y):

            val = img[i, j] * 50
            if val > 255:
                val = 255

            recup[i, j] = val

    cv.imshow('Imagen oscura', img)
    cv.imshow('Imagen recuperada (modo raw)', recup)

    cv.waitKey(0)
    cv.destroyAllWindows()


---
##  Análisis del Analista (Reflexiones Finales)

1. **Sobre los Operadores Puntuales (Misión 1):** Matemáticamente, ¿qué pasaría si en lugar de multiplicar por 50, hubieras sumado 50 a cada píxel oscuro? ¿Se revelaría el texto igual de claro o la imagen perdería contraste?
> *[Escribe tu respuesta aquí]*

2. **Sobre el Espacio HSV (Misión 4):** ¿Por qué el modelo de color BGR es ineficiente para la Recuperación de Información cuando buscamos "todos los tonos de azul celeste", y por qué el modelo HSV resuelve este problema con una sola variable?
> *[Escribe tu respuesta aquí]*

3. **Sobre Ecuaciones Paramétricas (Misión 5):** ¿Por qué las ecuaciones paramétricas (usando el parámetro t) son mejores para dibujar formas cerradas y complejas en graficación por computadora que usar la clásica función $y=f(x)$?
> *[Escribe tu respuesta aquí]*