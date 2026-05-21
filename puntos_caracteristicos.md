# Instituto Tecnológico de Morelia

---

**Materia:** Graficación  
**Profesor:** Jesus Eduardo Alcaraz Chavez  
**Alumno:** Diego Santiago Zavala Urueta  
**Número de control:** 24120396  
**Fecha:** 21 de mayo de 2025  

---

# Reporte de Investigación

## Algoritmos de Puntos Característicos SIFT, SURF y ORB: Aplicación en Realidad Aumentada y Deep Learning

---
---

## 1. Introducción

La visión por computadora es una de las disciplinas más activas dentro de las ciencias computacionales, y dentro de ella, la detección y descripción de puntos característicos representa uno de sus pilares fundamentales. Estos puntos, también conocidos como *keypoints* o *features*, son regiones de una imagen que concentran información relevante y estable, como esquinas, bordes con alta curvatura o estructuras locales únicas, que pueden ser identificadas de manera reproducible bajo distintas condiciones de captura.

En el contexto de la **Realidad Aumentada (RA)**, la detección de puntos característicos cumple un rol indispensable: permite que el sistema determine con precisión la posición y orientación de objetos reales en la escena, de modo que los elementos virtuales puedan superponerse de manera coherente y en tiempo real. Sin este proceso, sería imposible anclar objetos digitales al mundo físico con la estabilidad y precisión que la experiencia de RA requiere.

Los tres algoritmos que se analizan en este reporte —**SIFT** (Scale-Invariant Feature Transform), **SURF** (Speeded-Up Robust Features) y **ORB** (Oriented FAST and Rotated BRIEF)— representan la evolución histórica y técnica en esta área. Cada uno fue diseñado para superar las limitaciones de su predecesor: SIFT sentó las bases matemáticas, SURF optimizó la velocidad de cómputo, y ORB eliminó las restricciones de patentes al ofrecer una alternativa libre y eficiente.

Adicionalmente, el presente reporte aborda la integración de estas técnicas clásicas con el **aprendizaje profundo (Deep Learning)**, particularmente con arquitecturas como SuperPoint, que han demostrado superar en múltiples escenarios a los métodos tradicionales.

---

## 2. Conceptos Fundamentales de Puntos Característicos

### 2.1 ¿Qué es un punto característico?

Un punto característico es una región localizada de una imagen que presenta propiedades visuales suficientemente distintivas como para ser reconocida de forma consistente en múltiples imágenes de la misma escena, incluso cuando estas han sido capturadas desde diferentes ángulos, distancias, condiciones de iluminación o bajo transformaciones geométricas.

El proceso de trabajo con puntos característicos se divide en dos etapas:

1. **Detección (*detection*):** Se identifican las coordenadas espaciales de los puntos de interés dentro de la imagen.
2. **Descripción (*description*):** Para cada punto detectado, se genera un vector numérico —llamado descriptor— que codifica el contexto visual local alrededor de ese punto.

Estos descriptores son luego utilizados para realizar el **emparejamiento** (*matching*) entre puntos de diferentes imágenes, lo que permite estimar transformaciones geométricas, reconstruir la pose de la cámara y registrar el mundo real para la superposición de contenido virtual.

### 2.2 Propiedades deseables en un descriptor

Un descriptor de calidad debe ser:
- **Invariante a la escala:** Debe reconocer el mismo punto aunque la imagen sea capturada desde mayor o menor distancia.
- **Invariante a la rotación:** No debe cambiar si la imagen o el objeto es rotado.
- **Robusto a cambios de iluminación:** Su valor no debe variar drásticamente con diferentes condiciones de luz.
- **Discriminativo:** Debe distinguir claramente entre puntos diferentes.
- **Eficiente computacionalmente:** Para permitir procesamiento en tiempo real.

---

## 3. Algoritmo SIFT (Scale-Invariant Feature Transform)

### 3.1 Origen y propósito

SIFT fue desarrollado por **David Lowe** en 1999 y perfeccionado en 2004. Fue publicado con la idea de proponer un algoritmo capaz de extraer las características de una imagen y, a partir de estas, describir el conjunto de objetos contenidos en ella. Su principal aportación fue lograr detectores que son invariantes a cambios de escala y orientación, resistentes a variaciones parciales de iluminación y perspectiva.

### 3.2 Etapas del algoritmo

SIFT sigue un pipeline de cuatro etapas:

**a) Detección de extremos en el espacio de escala**  
Se construye una pirámide Gaussiana del image a múltiples resoluciones. Luego se calcula la *Diferencia de Gaussianas* (DoG), que aproxima al operador Laplaciano del Gaussiano. Los máximos y mínimos locales de esta función a través de diferentes escalas son los candidatos a puntos de interés, pues representan las características más estables.

**b) Localización y refinamiento de keypoints**  
Los puntos candidatos son refinados usando interpolación cuadrática tridimensional para ubicarlos con sub-precisión en el espacio de escala. Se descartan puntos con bajo contraste o ubicados en bordes poco definidos, filtrando mediante la relación de autovalores de la matriz Hessiana.

**c) Asignación de orientación dominante**  
Para cada keypoint, se calcula un histograma de orientaciones del gradiente en su vecindad. La orientación dominante se asigna como referencia canónica, haciendo al descriptor invariante a la rotación.

**d) Generación del descriptor SIFT**  
En la vecindad del keypoint (región de 16×16 píxeles), se calcula un conjunto de histogramas de orientaciones del gradiente organizados en una cuadrícula de 4×4 subregiones. Cada subregión genera un histograma de 8 orientaciones, resultando en un vector descriptor de **128 dimensiones**. Este vector se normaliza para mayor robustez ante cambios de iluminación.

### 3.3 Ventajas y limitaciones

SIFT es altamente preciso y robusto, siendo considerado durante años el estándar de referencia en detección de características. Sin embargo, su principal desventaja es el **alto costo computacional**: los descriptores de 128 dimensiones y el proceso de múltiples pasos lo hacen más lento y con mayor consumo de recursos que detectores modernos, dificultando su uso en aplicaciones de tiempo real. Adicionalmente, SIFT y SURF estaban protegidos por patentes comerciales, lo que limitó su libre distribución.

---

## 4. Algoritmo SURF (Speeded-Up Robust Features)

### 4.1 Origen y propósito

SURF fue propuesto por **Bay y Tuytelaars** en 2006 como una versión acelerada de SIFT. El algoritmo de SURF está basado en los mismos principios y pasos que SIFT, pero utiliza un esquema diferente que permite proveer resultados más rápidos manteniendo una robustez comparable. SURF obtuvo su nombre precisamente de su principal virtud: la velocidad computacional.

### 4.2 Innovaciones técnicas principales

**a) Detector Fast-Hessian**  
SURF usa el **determinante de la matriz Hessiana** como criterio de detección, debido a su buen rendimiento en tiempo de cálculo, precisión y robustez. En lugar de calcular la Gaussiana exacta, utiliza filtros de caja aproximados (*box filters*) que pueden evaluarse de manera extremadamente eficiente mediante **imágenes integrales** (también llamadas tablas de suma de área).

Las imágenes integrales permiten calcular la suma de píxeles en cualquier región rectangular en tiempo constante O(1), independientemente del tamaño de la región. Esto es fundamental para que SURF logre su velocidad característica.

**b) Descriptor SURF**  
El descriptor de SURF opera sobre una región de 4×4 subregiones de 5×5 píxeles. Para cada subregión calcula respuestas de wavelet de Haar en las direcciones horizontal y vertical. Esto genera un vector de **64 dimensiones**, la mitad que SIFT, lo que lo hace más rápido de calcular y comparar.

**c) Diferencias clave con SIFT**  
Mientras que SIFT almacena posición, escala y orientación para cada punto (permitiendo múltiples puntos en la misma posición a diferente escala), SURF en una posición (x,y) solo registra un único punto de interés, almacenando la matriz de segundo orden y el signo del Laplaciano en lugar de escala y orientación explícitas.

### 4.3 Ventajas y limitaciones

SURF es notablemente más rápido que SIFT al calcular descriptores de solo 64 dimensiones con filtros de caja eficientes. Sin embargo, comparativamente presenta menor precisión en algunos escenarios específicos. Al igual que SIFT, SURF estuvo sujeto a restricciones de patentes comerciales, lo que motivó el desarrollo de alternativas libres.

---

## 5. Algoritmo ORB (Oriented FAST and Rotated BRIEF)

### 5.1 Origen y propósito

En los laboratorios de OpenCV, **Ethan Rublee, Vincent Rabaud, Kurt Konolige y Gary R. Bradski** propusieron el algoritmo ORB como una alternativa a SIFT y SURF, permitiendo no solo escapar al problema de las patentes, sino también mejorando la eficiencia y consumo de recursos con la ventaja de permitirse su uso de forma gratuita. Su diseño se basa en la combinación de dos algoritmos para dos etapas diferenciadas.

### 5.2 Componentes del algoritmo

**a) Detección: FAST (Features from Accelerated Segment Test)**  
FAST es un detector de esquinas extremadamente rápido. Examina un círculo de 16 píxeles alrededor de cada píxel candidato: si un número suficiente de píxeles consecutivos en ese círculo son todos más brillantes o más oscuros que el píxel central (más un umbral), el punto es declarado esquina. ORB extiende FAST añadiendo **orientación** mediante el cálculo de momentos de imagen, haciendo al detector invariante a la rotación.

**b) Descripción: BRIEF (Binary Robust Independent Elementary Features)**  
BRIEF genera descriptores **binarios** (cadenas de bits). Compara pares de píxeles seleccionados aleatoriamente en la vecindad del keypoint y produce un 1 o 0 según cuál píxel sea más brillante. ORB aplica una rotación a los pares de puntos de BRIEF según la orientación calculada previamente (*Rotated BRIEF*), obteniendo invariancia rotacional.

El descriptor final de ORB tiene **32 dimensiones binarias** (equivalente a 256 bits), en contraste con los 128 floats de SIFT y los 64 floats de SURF. Esto lo hace no solo más compacto, sino también extremadamente rápido de comparar usando la distancia de Hamming.

### 5.3 Comparación cuantitativa de descriptores

| Característica | SIFT | SURF | ORB |
|---|---|---|---|
| Año de publicación | 1999/2004 | 2006 | 2011 |
| Dimensiones del descriptor | 128 floats | 64 floats | 32 bytes (binario) |
| Tipo de descriptor | Flotante | Flotante | Binario |
| Velocidad relativa | Lenta | Media | Rápida |
| Licencia | Patentado* | Patentado* | Libre (BSD) |
| Invariancia a escala | Sí | Sí | Parcial |
| Invariancia a rotación | Sí | Sí | Sí |

*SIFT y SURF expiraron sus patentes originales alrededor de 2020.

---

## 6. Aplicación en Realidad Aumentada

### 6.1 Pipeline general de RA basado en características

El proceso de realidad aumentada sin marcadores fiduciales (o *markerless AR*) basado en características visuales sigue el siguiente flujo:

1. **Captura de imagen:** La cámara del dispositivo captura el fotograma actual.
2. **Detección de keypoints:** Se aplica el algoritmo elegido (SIFT, SURF u ORB) para identificar puntos de interés en el fotograma.
3. **Cálculo de descriptores:** Para cada keypoint se calcula su vector descriptor.
4. **Emparejamiento (*matching*):** Los descriptores del fotograma se comparan contra una base de datos de descriptores de la imagen de referencia del objeto, usando algoritmos como Brute-Force o FLANN (Fast Library for Approximate Nearest Neighbors).
5. **Estimación de homografía:** Con los pares de puntos emparejados, se calcula la homografía usando RANSAC para eliminar falsos emparejamientos (*outliers*).
6. **Cálculo de pose:** La homografía permite estimar la posición y orientación (pose) de la cámara respecto al objeto real mediante la matriz de pose.
7. **Renderizado:** Con la pose calculada, se renderiza el objeto virtual en las coordenadas correctas del mundo real.

### 6.2 ORB como opción preferida en RA móvil

Los algoritmos de detección de características son computacionalmente demandantes, y en dispositivos móviles con recursos limitados esta restricción es crítica. Por ello, ORB se ha convertido en la opción preferida para aplicaciones de RA en tiempo real. Según la documentación oficial de OpenCV, todos los métodos de detección mencionados son buenos en algún sentido, pero no son lo suficientemente rápidos para aplicaciones en tiempo real como SLAM, motivo por el que se diseñó ORB.

En experimentos comparativos, ORB permite procesar video a tasas superiores a 30 fps en dispositivos móviles modernos, mientras que SIFT puede reducir esta tasa significativamente al ser más costoso computacionalmente.

### 6.3 Caso de uso: sistema de RA para capacitación industrial

En investigaciones de instituciones mexicanas como el repositorio del CIO (Centro de Investigaciones en Óptica), se ha demostrado la aplicación práctica de estos tres algoritmos en sistemas de realidad aumentada para capacitación industrial. En estos sistemas, se evaluaron SIFT, SURF y ORB aplicados a marcadores con distintos niveles de varianza visual, capturados a diferentes distancias y condiciones de iluminación. Los resultados mostraron que ORB ofrece el mejor compromiso entre velocidad de procesamiento y robustez para este tipo de aplicaciones.

### 6.4 Marcos de trabajo populares

Los siguientes frameworks integran internamente técnicas similares a las descritas:

- **ARToolKit:** Biblioteca de código abierto y multiplataforma para RA. Procesa datos gráficos de la cámara en tiempo de ejecución, detecta marcadores y superpone objetos 3D. Integra capacidades de seguimiento de características naturales.
- **Vuforia:** SDK comercial ampliamente utilizado en entornos industriales. Usa una puntuación de evaluación de marcadores basada en la riqueza de características detectables en la imagen.
- **ARCore (Google) y ARKit (Apple):** Plataformas modernas de RA para Android e iOS que implementan variantes altamente optimizadas de detección de características para seguimiento de superficies, estimación de luz y anclaje de objetos.
- **OpenCV + Python/C++:** Permite implementar pipelines de RA personalizados usando directamente SIFT, SURF u ORB. Es común en proyectos educativos y de investigación.

---

## 7. Deep Learning y Puntos Característicos

### 7.1 ¿Por qué el Deep Learning?

Aunque los algoritmos clásicos como SIFT, SURF y ORB han demostrado ser altamente efectivos durante décadas, presentan limitaciones en escenarios extremos: cambios severos de iluminación, texturas repetitivas, deformaciones no rígidas o vistas muy diferentes del mismo objeto. El **aprendizaje profundo** ofrece la capacidad de aprender representaciones desde datos, potencialmente superando las restricciones de los descriptores diseñados a mano.

### 7.2 SuperPoint: la evolución hacia Deep Learning

**SuperPoint** es una de las propuestas más influyentes en la intersección entre detección de características y redes neuronales. Es una arquitectura *encoder-decoder* entrenada de forma auto-supervisada que realiza simultáneamente la detección de keypoints y el cálculo de descriptores densos en una sola pasada hacia adelante (*forward pass*), pudiendo ejecutarse en tiempo real.

Su proceso de entrenamiento tiene tres etapas:
1. Un detector base (*MagicPoint*) aprende a detectar keypoints en el dataset de *Synthetic Shapes*.
2. Se aplica *Homographic Adaptation* para expandir la capacidad de detección a imágenes reales mediante auto-supervisión.
3. Se entrena el módulo descriptor en la tarea de emparejamiento de imágenes.

En cuanto a velocidad, SuperPoint toma menos tiempo que SIFT y es equivalente a ORB, mientras que después de optimización en hardware puede ejecutarse a 20 fps o más.

### 7.3 FeatureBooster: potenciando descriptores clásicos con redes ligeras

Una propuesta muy práctica es **FeatureBooster**, una red neuronal ligera que toma los descriptores de ORB o SIFT ya calculados y los mejora mediante una red Transformer, sin necesidad de recalcularlos desde cero. El método requiere solo 3.2 ms en GPU de escritorio y 27 ms en GPU embebida para procesar 2000 features, siendo suficientemente rápido para sistemas prácticos. Los resultados muestran que ORB mejorado con FeatureBooster supera significativamente al ORB crudo en escenarios de cambios de iluminación y patrones repetitivos.

### 7.4 Otras arquitecturas de interés

- **LIFT (Learned Invariant Feature Transform):** Reemplaza el pipeline SIFT completo (detección, estimación de orientación, descripción) con redes convolucionales. Requiere supervisión de un sistema SfM clásico.
- **D2-Net y R2D2:** Integran la detección y descripción en un único mapa de características, sin separar ambas etapas.
- **Reinforced SuperPoint:** Variante de SuperPoint entrenada mediante aprendizaje por refuerzo que alcanza y supera ligeramente la precisión de SIFT en tareas de estimación de pose relativa.

### 7.5 Comparativa clásico vs. deep learning

| Aspecto | SIFT/SURF/ORB | SuperPoint / Deep Learning |
|---|---|---|
| Diseño | Manual (handcrafted) | Aprendido de datos |
| Generalización | Buena en condiciones normales | Mejor en casos extremos |
| Velocidad | Muy rápida (ORB) | Comparable (requiere GPU) |
| Requerimientos | Solo CPU | Preferiblemente GPU |
| Entrenamiento necesario | No | Sí |
| Explicabilidad | Alta | Baja (caja negra) |

---

## 8. Implementación Práctica con OpenCV

A continuación se presenta un fragmento representativo del proceso en Python usando ORB para una aplicación de RA básica:

```python
import cv2
import numpy as np

# Cargar imagen de referencia
img_ref = cv2.imread('objeto_referencia.jpg', cv2.IMREAD_GRAYSCALE)

# Inicializar detector ORB
orb = cv2.ORB_create(nfeatures=500)

# Detectar y calcular descriptores en la imagen de referencia
kp_ref, des_ref = orb.detectAndCompute(img_ref, None)

# Inicializar matcher Brute-Force con distancia Hamming (adecuada para ORB binario)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Capturar video de la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar keypoints en el fotograma actual
    kp_frame, des_frame = orb.detectAndCompute(gray, None)
    
    if des_frame is not None:
        # Emparejar descriptores
        matches = bf.match(des_ref, des_frame)
        matches = sorted(matches, key=lambda x: x.distance)
        
        # Tomar los mejores 50 matches
        good_matches = matches[:50]
        
        if len(good_matches) > 10:
            # Extraer coordenadas de los puntos emparejados
            pts_ref = np.float32([kp_ref[m.queryIdx].pt for m in good_matches])
            pts_frame = np.float32([kp_frame[m.trainIdx].pt for m in good_matches])
            
            # Calcular homografía con RANSAC
            H, mask = cv2.findHomography(pts_ref, pts_frame, cv2.RANSAC, 5.0)
            
            # Aquí se proyectan los objetos virtuales usando H
            # ...
    
    cv2.imshow('AR Demo', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

Este pipeline ilustra la cadena completa: captura → detección → descripción → emparejamiento → homografía → pose, que es la base de cualquier sistema de RA basado en características visuales.

---

## 9. Conclusiones

El estudio de los algoritmos de puntos característicos SIFT, SURF y ORB revela una evolución constante orientada a satisfacer las demandas de precisión, velocidad y accesibilidad que las aplicaciones modernas de visión por computadora exigen. Cada algoritmo representa un avance significativo sobre su predecesor: SIFT estableció los fundamentos matemáticos de la invariancia a escala y orientación con descriptores de alta dimensionalidad; SURF los aceleró mediante aproximaciones eficientes con imágenes integrales y filtros de caja; y ORB democratizó el acceso al combinar FAST y BRIEF en una solución libre, binaria y extremadamente veloz.

En el contexto de la **Realidad Aumentada**, estos algoritmos son la columna vertebral de los sistemas que no dependen de marcadores fiduciales. Su capacidad para detectar y emparejar características visuales estables entre fotogramas consecutivos permite estimar la pose de la cámara en tiempo real, condición indispensable para anclar objetos virtuales al mundo físico con fidelidad. La elección del algoritmo depende del hardware disponible: en dispositivos móviles de recursos limitados, ORB resulta la opción más práctica; en sistemas con mayor capacidad de cómputo, SIFT puede ofrecer mayor precisión.

La integración con **Deep Learning** abre una nueva dimensión en este campo. Arquitecturas como SuperPoint demuestran que las redes neuronales pueden aprender representaciones de características más robustas que los descriptores diseñados manualmente, especialmente en condiciones extremas de iluminación, perspectiva o textura. Herramientas como FeatureBooster ilustran que no es necesario abandonar los algoritmos clásicos: basta con potenciar sus descriptores con redes ligeras para obtener mejoras sustanciales. El futuro apunta hacia sistemas híbridos que combinen la eficiencia de ORB con la robustez aprendida de las CNN, ejecutables en tiempo real incluso en hardware embebido.

Como reflexión final, el dominio de estas técnicas no solo es relevante para la RA, sino para toda la cadena de aplicaciones de visión computacional: SLAM (Simultaneous Localization and Mapping), reconstrucción 3D, robots autónomos, inspección industrial y sistemas de navegación. Comprender sus fundamentos matemáticos y prácticos es, por tanto, una competencia esencial para cualquier ingeniero que trabaje en el cruce entre software, visión artificial y el mundo físico.

---

## Referencias

- Lowe, D. G. (2004). *Distinctive Image Features from Scale-Invariant Keypoints*. International Journal of Computer Vision, 60(2), 91–110.
- Bay, H., Tuytelaars, T., & Van Gool, L. (2006). *SURF: Speeded Up Robust Features*. European Conference on Computer Vision (ECCV).
- Rublee, E., Rabaud, V., Konolige, K., & Bradski, G. (2011). *ORB: An Efficient Alternative to SIFT or SURF*. International Conference on Computer Vision (ICCV).
- DeTone, D., Malisiewicz, T., & Rabinovich, A. (2018). *SuperPoint: Self-Supervised Interest Point Detection and Description*. CVPR Workshops.
- Zhang, J., et al. (2022). *FeatureBooster: Boosting Feature Descriptors with a Lightweight Neural Network*. arXiv:2211.15069.
- Repositorio Institucional CIO. *Sistema de Realidad Aumentada para la Capacitación en un Torno Industrial*. Centro de Investigaciones en Óptica, México.
- Scielo Chile. (2020). *Algoritmos de rastreo de movimiento utilizando técnicas de descriptores*. Información Tecnológica, 31(3).
- OpenCV Documentation. *Feature Detection and Description*. https://docs.opencv.org/4.x/
- Wikipedia Español. *SURF (algoritmo)*. https://es.wikipedia.org/wiki/SURF
- Ultralytics Blog. (2025). *Algoritmo SIFT: cómo funciona la correspondencia de características*.